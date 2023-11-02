"""The IAM Bindings CLI command module."""
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape


jinja_env = Environment(loader=PackageLoader("dapla_team_cli.tf.iam_bindings"), autoescape=select_autoescape())


class MissingUserSuppliedInfoError(Exception):
    """Exception that could occur if a user did not supply enough information for a command to execute."""
