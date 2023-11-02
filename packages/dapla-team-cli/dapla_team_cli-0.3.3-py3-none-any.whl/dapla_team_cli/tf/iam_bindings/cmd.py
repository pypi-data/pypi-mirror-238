"""IAM Bindings CLI command definition."""
import logging
import os
import shutil
import sys
import time
from io import TextIOWrapper
from typing import Any
from typing import List
from typing import Optional
from typing import Union

import git
import questionary as q
import typer
from rich.console import Console
from rich.style import Style
from rich.tree import Tree

from dapla_team_cli import github
from dapla_team_cli.config import get_config_folder_path
from dapla_team_cli.team import TeamRepoInfo
from dapla_team_cli.team import get_remote_from_name
from dapla_team_cli.team import get_team_name
from dapla_team_cli.tf.iam_bindings import MissingUserSuppliedInfoError
from dapla_team_cli.tf.iam_bindings import jinja_env
from dapla_team_cli.tf.iam_bindings.auth_groups import ask_for_auth_group_name
from dapla_team_cli.tf.iam_bindings.buckets import ask_for_buckets
from dapla_team_cli.tf.iam_bindings.configs import AuthGroupIAMConfig
from dapla_team_cli.tf.iam_bindings.configs import BucketIAMConfig
from dapla_team_cli.tf.iam_bindings.configs import EnvironmentIAMConfig
from dapla_team_cli.tf.iam_bindings.configs import IAMBindingConfig
from dapla_team_cli.tf.iam_bindings.configs import RoleIAMConfig
from dapla_team_cli.tf.iam_bindings.environments import ask_for_environments
from dapla_team_cli.tf.iam_bindings.expiry import ask_for_expiry
from dapla_team_cli.tf.iam_bindings.project_roles import ask_for_project_roles
from dapla_team_cli.tf.iam_bindings.terraform import write_tf_files
from dapla_team_cli.tf.iam_bindings.utilities import igroupby


console = Console(record=True, width=100)

logger = logging.getLogger("dpteam")

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
    "success": Style(color="green", blink=True, bold=True),
}


def iam_bindings(
    auth_group: Optional[str] = typer.Option(  # noqa: B008
        None,
        "--auth-group",
        "-g",
        help='Name of "auth group", such as demo-enhjoern-a-support',
    ),
    push_to_github: bool = typer.Option(  # noqa: B008
        True,
        "--github/--no-github",
        help="True if the changes should be be pushed as a branch to GitHub",
    ),
    source_config_file: Optional[typer.FileBinaryRead] = typer.Option(  # noqa: B008
        None,
        "--source-config",
        help="Read config from json instead of prompting interactively",
    ),
    target_config_file: Optional[typer.FileTextWrite] = typer.Option(  # noqa: B008
        None,
        "--target-config",
        help="Name of target config json file (if you later want to replay without interactive prompting)",
    ),
    team_name: str = typer.Option(  # noqa: B008
        "", "--team-name", "-t", help="Name of the team you want to create bindings for (without -iac suffix)"
    ),
) -> None:
    """Create IAM Binding Terraform files that assign roles and permissions to a group of Dapla users.

    You are prompted to supply information such as name of the group, environments, project roles, bucket roles
    and also a timeframe that the IAM binding should be constrained by. Terraform files are then created, one for each
    environment and auth group, keeping configuration neatly grouped and separated.

    \b
    Example:
        Let's say you want the support group of a team (e.g. `demo-enhjoern-a`) to be able to administer Secret Manager
        for a limited amount of time in both `staging` and `prod` environments. The output from this command would then
        be two files: `iam-support-staging.tf` and `iam-support-prod.tf`.

    Note that the command is strictly working with _one_ auth group. You need to run the command multiple times if you
    want to create IAM bindings for multiple groups. Alternatively, you can record the config and re-run in
    non-interactive mode, only changing the name of the auth group between executions.
    """
    config_folder_path = get_config_folder_path(tmp=True)
    logger.debug("using config folder path: %s", config_folder_path)
    g = git.cmd.Git(config_folder_path)

    if not team_name:
        team_name = get_team_name()

    repo_info = get_remote_from_name(team_name)
    logger.debug("repo_info: %s", repo_info.__dict__)

    console.print(
        f"Cloning a copy of {team_name} from {repo_info.remote_url} into temporary folder...",
        style=styles["normal"],
    )

    g.execute(["git", "clone", f"{repo_info.remote_url}", f"{repo_info.clone_folder}"])

    console.print(
        "Cloning complete. Temporary files will automatically be removed after this command has finished running.",
        style=styles["normal"],
    )

    if source_config_file:
        config_json = source_config_file.read()
        config = IAMBindingConfig.parse_raw(config_json)
    else:
        try:
            config = ask_for_config(repo_info, auth_group)
        except MissingUserSuppliedInfoError as e:
            bail_out(str(e), 1)

    if not config:
        print("No configuration given, aborting...")
        typer.Abort()

    combine_configs(config)

    target_tf_files = write_tf_files(config, target_path=repo_info.clone_folder)

    tree = print_summary(config, target_tf_files)

    if target_config_file:
        target_config_file.write(config.json())

    if push_to_github:
        create_git_branch(repo_path=repo_info.clone_folder, config=config, files=target_tf_files, tree=tree)

    cleanup_iac_temp_folder(repo_info.clone_folder)


def combine_configs(config: IAMBindingConfig) -> None:
    """Combine all configurations."""
    config.combine()
    for auth_group in config.auth_groups:
        auth_group.combine()
        for env in auth_group.envs:
            env.combine()


def ask_for_config(repo_info: TeamRepoInfo, auth_group: Optional[str]) -> IAMBindingConfig:
    """Ask the user for configuration used to generate the bindings. Supports multiple auth groups."""
    authgroup_configs = []

    more_config = True
    while more_config:
        authgroup_configs.append(ask_for_authgroup_config(repo_info, auth_group))
        more_config = q.confirm("Do you want to configure bindings for another auth group?").ask()
        # In case auth group was supplied, set to None so it asks for a new auth group next time
        auth_group = None

    rationale = ask_for_rationale()
    return IAMBindingConfig(team_name=repo_info.name, auth_groups=authgroup_configs, rationale=rationale)


def create_git_branch(repo_path: str, config: IAMBindingConfig, files: List[TextIOWrapper], tree: str) -> None:
    """Push a new branch with the generated IAM bindings files to GitHub.

    Create a git branch with a descriptive name and detailed commit message.

    Args:
        repo_path: path to a local clone of the IaC git repo
        config: user preferences
        files: the Terraform IAM binding files that should be applied through a new PR
        tree: plain-text version of the summary rich.Tree which is displayed after running iam-bindings
    """
    environments = "-and-".join({env.name for group in config.auth_groups for env in group.envs})
    auth_groups = "+".join({group.shortname for group in config.auth_groups})
    branch_name = f"iam-bindings-for-{auth_groups}-in-{environments}-{int(time.time())}"
    template = jinja_env.get_template("iam-bindings-git-commit-msg.jinja")
    commit_msg = template.render(
        environments={e.name for ag in config.auth_groups for e in ag.envs}, rationale=config.rationale, tree=tree.strip()
    )
    pr_url = f"https://github.com/statisticsnorway/{config.team_name}-iac/pull/new/{branch_name}"
    instruction_msg = (
        f"A new branch called {branch_name} has been pushed to GitHub.\n"
        "Create a pull request and issue an 'atlantis apply'-comment in order to effectuate the IAM bindings.\n"
        f"Use this link to create a pull request: {pr_url}"
    )
    b = github.NewBranch(
        repo_path=repo_path,
        branch_name=branch_name,
        commit_msg=commit_msg,
        files={f.name for f in files},
        instruction_msg=instruction_msg,
    )
    github.create_branch(b)


def ask_for_authgroup_config(repo_info: TeamRepoInfo, auth_group_name: Optional[str]) -> AuthGroupIAMConfig:
    """Ask the user for configuration used to generate IAM binding Terraform files.

    Args:
        repo_info: TeamRepoInfo object containing info about the team's IaC repo, in this function the team's repo path is used.
        auth_group_name: Name of an auth group. If not specified, then the user is prompted explicitly for this.

    Returns:
        User supplied config used to generate IAM Terraform files

    Raises:
        MissingUserSuppliedInfoError: if the user failed to specify enough information (such as at least one environment)
    """
    team = repo_info.name

    if auth_group_name is None:
        auth_group_name = ask_for_auth_group_name(team)
    auth_group_shortname = auth_group_name.replace(f"{team}-", "")

    project_roles = ask_for_project_roles(auth_group_name)
    buckets = ask_for_buckets(team, auth_group_name)

    if not (project_roles or buckets):
        raise MissingUserSuppliedInfoError("No roles or buckets specified, nothing to do...")

    environments = ask_for_environments()
    if not environments:
        raise MissingUserSuppliedInfoError("No environments specified, nothing to do...")

    expiry = ask_for_expiry()

    env_configs = []
    for env in environments:
        buckets_config = [BucketIAMConfig(name=b.simple_name, access=b.access_type, expiry=expiry) for b in buckets]
        roles_config = [RoleIAMConfig(role=r, expiry=expiry) for r in project_roles]
        env_configs.append(EnvironmentIAMConfig(name=env, buckets=buckets_config, roles=roles_config))

    return AuthGroupIAMConfig(name=auth_group_name, shortname=auth_group_shortname, envs=env_configs)


def cleanup_iac_temp_folder(iac_repo_clone_path: str) -> None:
    """Cleans up temporary files in the .config folder that were cloned from github.

    Args:
        iac_repo_clone_path: Path to the cloned IaC repo (i.e the temporary files).
    """
    console.print("Cleaning up temporary files...", style=styles["normal"])

    if os.path.exists(iac_repo_clone_path):
        shutil.rmtree(iac_repo_clone_path)
    else:
        console.print(
            f"Failed to remove temporary files at {iac_repo_clone_path}. File was not correctly created or has been moved.",
            style=styles["warning"],
        )
        sys.exit(1)

    console.print("Succesfully removed temporary files", style=styles["success"])


def ask_for_rationale() -> Any:
    """Ask the user for a reason for adding the IAM bindings.

    This text is included in the commit message and serves as an audit log.

    Returns:
        User-supplied rationale for adding the IAM bindings
    """
    return q.text("Why is the access needed?").ask()


def bail_out(message: str, exit_code: int = 1) -> None:
    """Print an exit message and exit the command with a status code.

    Args:
        message: The message to print when exiting.
        exit_code: Exit code to use when exiting. 0 means ok.
    """
    print(message)
    sys.exit(exit_code)


def summarise_env(env: EnvironmentIAMConfig, team_name: str) -> Tree:
    """Generate the summary for one environment.

    Args:
        env: The user supplied configuration for a specific environment.
        team_name: The team's name.
    """
    env_tree = Tree(f"🌤  [bold bright_white]Environment: {env.name}")
    combined_configs: List[Union[BucketIAMConfig, RoleIAMConfig]] = env.roles + env.buckets
    role_and_buckets = igroupby(combined_configs, lambda x: x.expiry)

    for exp, configs in role_and_buckets.items():
        exp_t = env_tree.add(f"📅 [bold bright_white]Timeframe:[/] {exp.name} [bright_black]({exp.timestamp})")
        configs_list = list(configs)
        buckets = [config for config in configs_list if isinstance(config, BucketIAMConfig)]
        roles = [config for config in configs_list if isinstance(config, RoleIAMConfig)]
        if roles:
            project_roles = exp_t.add("🧢 [bold bright_white]Project Roles")
            for role in roles:
                project_roles.add(f"{role.role.title} [bright_black]({role.role.name})")

        if buckets:
            bucket_tree = exp_t.add("🪣 [bold bright_white]Buckets")
            for bucket in buckets:
                bucket_tree.add(f"ssb-{env.name}-{team_name}-{bucket.name} [bucketright_bucketlack]({bucket.access})")

    return env_tree


def print_summary(config: IAMBindingConfig, target_tf_files: List[TextIOWrapper]) -> str:
    """Print a summary of the executed command, detailing the user's choices and the resulting files.

    Args:
        config: The user supplied configuration that was used.
        target_tf_files: The generated Terraform files.
    """
    tree = Tree(f"📎 [bold reverse]IAM bindings for [italic]{config.team_name}")
    for auth_group in config.auth_groups:
        ag = tree.add(f"👥 [italic]{auth_group.name}")
        # tree.add(f"🔩 [bold bright_white]GCP Projects:[/] {', '.join(config.gcp_projects)}")
        for env in auth_group.envs:
            ag.add(summarise_env(env, config.team_name))

    if target_tf_files:
        tf_files = tree.add("📄 [bold bright_white]Terraform files")
        for tf_file in target_tf_files:
            tf_files.add(f"[link=file:///{tf_file.name}]{os.path.basename(tf_file.name)}[/link]")

    # Clear "record buffer"
    console.export_text()
    console.print(tree)
    return console.export_text()
