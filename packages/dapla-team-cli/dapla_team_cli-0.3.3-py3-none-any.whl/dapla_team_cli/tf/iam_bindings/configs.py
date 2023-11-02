"""Contains classes representing user provided configs for different levels (group, env, bucket/role) of the wanted iam bindings."""
from typing import List
from typing import Tuple

from pydantic import BaseModel

from dapla_team_cli.gcp import GCPRole
from dapla_team_cli.tf.iam_bindings.expiry import Expiry
from dapla_team_cli.tf.iam_bindings.utilities import combine_and_maximize
from dapla_team_cli.tf.iam_bindings.utilities import igroupby


class BucketIAMConfig(BaseModel):
    """Represents one bucket IAM binding."""

    name: str
    access: str
    expiry: Expiry

    def identifier(self) -> Tuple[str, str]:
        """A bucket config is identified by its name and access type."""
        return (self.name, self.access)

    def sorter(self) -> str:
        """Sort bucket configs based on the expiry timestamp."""
        return self.expiry.timestamp


class RoleIAMConfig(BaseModel):
    """Represents one project role IAM binding."""

    role: GCPRole
    expiry: Expiry

    def identifier(self) -> GCPRole:
        """A role config is identified by its role."""
        return self.role

    def sorter(self) -> str:
        """Sort role configs based on the expiry timestamp."""
        return self.expiry.timestamp


class EnvironmentIAMConfig(BaseModel):
    """Represents IAM Config for one environment for one auth group."""

    name: str
    buckets: List[BucketIAMConfig]
    roles: List[RoleIAMConfig]

    def combine(self) -> None:
        """Combine buckets and roles if they share the same name, and choose the one with the longest expiry."""
        self.buckets = combine_and_maximize(self.buckets)
        self.roles = combine_and_maximize(self.roles)


class AuthGroupIAMConfig(BaseModel):
    """Represents IAM config for one auth group."""

    name: str
    shortname: str
    envs: List[EnvironmentIAMConfig]

    def combine(self) -> None:
        """Combine EnvironmentIAMConfigs if they are the same env."""
        combined_envs = []
        same_env = igroupby(self.envs, lambda e: e.name)
        for env, confs in same_env.items():
            buckets: List[BucketIAMConfig] = []
            roles: List[RoleIAMConfig] = []
            for conf in confs:
                buckets = buckets + conf.buckets
                roles = roles + conf.roles
            combined_envs.append(EnvironmentIAMConfig(name=env, buckets=buckets, roles=roles))

        self.envs = combined_envs


class IAMBindingConfig(BaseModel):
    """Represents the overall IAM binding config to commit."""

    team_name: str
    auth_groups: List[AuthGroupIAMConfig]
    rationale: str

    def combine(self) -> None:
        """Combine multiple AuthGroupIAMConfigs into a single one if they represent the same auth group."""
        combined_groups = []

        same_group = igroupby(self.auth_groups, lambda g: (g.name, g.shortname))
        for group, confs in same_group.items():
            envs: List[EnvironmentIAMConfig] = []
            for conf in confs:
                envs = envs + conf.envs
            combined_groups.append(AuthGroupIAMConfig(name=group[0], shortname=group[1], envs=envs))

        self.auth_groups = combined_groups
