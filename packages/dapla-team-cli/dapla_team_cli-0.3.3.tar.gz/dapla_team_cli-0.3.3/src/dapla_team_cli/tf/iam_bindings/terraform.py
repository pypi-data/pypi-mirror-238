"""Module that contains terraform related functions."""
import os
import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import hcl2
from rich.console import Console
from rich.style import Style

from dapla_team_cli.tf.iam_bindings import jinja_env
from dapla_team_cli.tf.iam_bindings.configs import IAMBindingConfig
from dapla_team_cli.tf.iam_bindings.utilities import igroupby


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


def write_tf_files(config: IAMBindingConfig, target_path: str) -> List[Any]:
    """Produce and write terraform files to `target_path`.

    Args:
        config: user supplied configuration
        target_path: The path to write files to

    Returns:
        a list of terraform files that was written
    """
    # Create terraform files - one file per auth group and environment
    tf_files = create_tf_files(config, target_path)
    target_tf_files = []

    # Write the files to the team's IaC repo
    for tf_file_name, content in tf_files.items():
        file_path = os.path.join(target_path, tf_file_name)
        with open(file_path, mode="w", encoding="utf-8") as tf_file:
            tf_file.write(content)
            target_tf_files.append(tf_file)

    return target_tf_files


def get_iam_module_name(shortname: str, environment: str) -> str:
    """Get name of iam-bindings module for the given auth group and environment."""
    return f"projects-iam-{shortname}-{environment}"


def get_bucket_module_name(shortname: str, env: str, name: str) -> str:
    """Get name of the iam module for the given group, environment and bucket."""
    return f"buckets-{shortname}-iam-{env}-{name}"


def get_module(modules: Any, module_name: str) -> Optional[Any]:
    """Return the module asked for, or return None."""
    for module in modules:
        if module_name in module:
            return module

    return None


def get_old_bindings(hcl_object: Dict[Any, Any], module_name: str) -> List[Any]:
    """Get already-existing bindings, so that we can avoid overwriting them."""
    # if not os.path.exists(bindings_file):
    #     return []

    # with open(bindings_file, encoding="utf-8") as f:
    if "module" not in hcl_object:
        return []

    module = get_module(hcl_object["module"], module_name)
    if module is None:
        return []

    return list(module[module_name]["conditional_bindings"])


def module_regex(module_name: str) -> str:
    """Returns regex to match a Terraform module block."""
    return rf'module "{module_name}" {{(?:\n(?: [ ]+.*$)*)+\n}}'


def create_tf_files(config: IAMBindingConfig, target_path: str) -> Dict[str, str]:
    """Create Terraform files (iam-bindings) based on user-specified resource configuration.

    Args:
        config: IAMBindingConfig collected from user that specifies which resources to
            generate Terraform IAM bindings for
        target_path: Path to the (temporary) git repo where the tf files should be written

    Returns:
        An IAMBindingConfig (filename -> tf file content)

    """
    # TODO: Refactor this function..
    tf_files = {}

    bucket_template = jinja_env.get_template("buckets-iam.jinja")
    project_iam_template = jinja_env.get_template("projects-iam.jinja")

    for auth_group in config.auth_groups:
        for env in auth_group.envs:
            filename = f"iam-{auth_group.shortname}-{env.name}.tf"
            filepath = os.path.join(target_path, filename)

            # Projects IAM binding module name
            iam_module = get_iam_module_name(auth_group.shortname, env.name)

            # Find old bindings in file if it exists
            old_bindings = []
            old_buckets = {}
            old_content = ""
            if os.path.exists(filepath):
                with open(filepath, encoding="utf-8") as f:
                    old_content = f.read()
                    hcl_object = hcl2.loads(old_content)

                    # Old projects IAM bindings
                    old_bindings = get_old_bindings(hcl_object, iam_module)
                    # Overwrite old bindings if role name matches
                    new_roles = [r.role.name for r in env.roles]
                    old_bindings = [r for r in old_bindings if r["role"] not in new_roles]

                    # Old bucket bindings
                    for bucket in {b.name for b in env.buckets}:
                        module_name = get_bucket_module_name(auth_group.name, env.name, bucket)
                        old_buckets[bucket] = get_old_bindings(hcl_object, module_name)
                        new_binding_roles = [b.access for b in env.buckets if b.name == bucket]
                        old_buckets[bucket] = [b for b in old_buckets[bucket] if b["role"].split(".")[-1] not in new_binding_roles]

            if env.roles:
                projects_iam = project_iam_template.render(auth_group=auth_group, env=env, old_bindings=old_bindings)
                pattern = re.compile(module_regex(iam_module), flags=re.MULTILINE)
                if pattern.search(old_content):
                    old_content = pattern.sub(projects_iam, old_content)
                else:
                    old_content = "\n".join((old_content, projects_iam))

            for bucket, bindings in igroupby(env.buckets, lambda b: b.name).items():
                module_name = get_bucket_module_name(auth_group.name, env.name, bucket)

                bucket_iam = bucket_template.render(
                    bucket=bucket,
                    auth_group=auth_group,
                    env=env.name,
                    bucket_bindings=bindings,
                    old_bindings=old_buckets.get(bucket, []),
                    team_name=config.team_name,
                )
                pattern = re.compile(module_regex(module_name), flags=re.MULTILINE)
                if pattern.search(old_content):
                    old_content = pattern.sub(bucket_iam, old_content)
                else:
                    old_content = "\n".join((old_content, bucket_iam))

            tf_files[filename] = old_content
    return tf_files
