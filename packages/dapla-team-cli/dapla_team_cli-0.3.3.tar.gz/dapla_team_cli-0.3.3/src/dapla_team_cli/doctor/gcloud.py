"""Checks for gcloud and homebrew installations."""
import logging
import subprocess
from shutil import which
from sys import platform

import questionary as q

from dapla_team_cli.doctor.check import Check
from dapla_team_cli.doctor.check import Failure
from dapla_team_cli.doctor.check import Success


logger = logging.getLogger("dpteam")


def check_brew() -> Check:
    """Check if Homebrew is installed."""
    brew_exists = which("brew") is not None

    if not brew_exists:
        failure = "\n".join(
            [
                "You are using MacOS, but you seem to be missing Homebrew...🍺",
                "Please install Homebrew (https://brew.sh/) and verify your "
                "installation by running 'brew doctor'. Then rerun this command.",
            ]
        )
        return Failure(message=failure)

    brew_version = subprocess.run(["brew", "--version"], text=True, capture_output=True, check=True)

    if brew_version.stderr:
        logger.debug("brew_version.stderr: %s", brew_version.stderr)
        return Failure(
            message=(
                "❌ The gcloud CLI is missing. Either install it using Homebrew (https://brew.sh/) or manually "
                "   using the official installation instructions at https://cloud.google.com/sdk/docs/install"
            )
        )

    logger.debug("brew_version.stdout: %s", brew_version.stdout)
    success = brew_version.stdout.split("\n")[0]
    return Success(message=success)


def mac_install_gcloud() -> Check:
    """Install gcloud CLI."""
    has_brew = check_brew()
    if not has_brew:
        return has_brew

    gcloud_permission = q.confirm("The gcloud CLI is missing, do you want to install it?").ask()
    if not gcloud_permission:
        return Failure(message="❌ Homebrew is installed, but you chose not to install the gcloud CLI")

    print("Installing the gcloud CLI...")

    gcloud_installer = subprocess.run(
        ["brew", "install", "--cask", "google-cloud-sdk"],
        capture_output=False,
        text=True,
        shell=False,
        check=True,
    )

    if gcloud_installer.stderr:
        logger.debug("gcloud_installer.stderr: %s", gcloud_installer.stderr)
        return Failure(message="❌ Error installing the gcloud CLI")

    gcloud_version = subprocess.run(["gcloud", "--version"], capture_output=True, text=True, shell=False, check=True)

    if gcloud_version.stderr:
        logger.debug("gcloud_version.stderr: %s", gcloud_version.stderr)
        return Failure(
            message=(
                "❌ gcloud installation seemingly succeeded, but gcloud is still not available.\n   Try restarting your terminal."
            ),
        )

    logger.debug("gcloud_version.stdout: %s", gcloud_version.stdout)
    return Success(message="✅ gcloud CLI installed and available")


def check_gcloud() -> Check:
    """Check if the gcloud CLI is installed."""
    gcloud_exists = which("gcloud")
    if gcloud_exists:
        logger.debug("gcloud exists at %s", gcloud_exists)
        return Success(message="✅ gcloud CLI installed")

    if platform != "darwin":
        logger.debug("platform is not macos -> auto-install not implemented")
        return Failure(
            message=(
                "❌ The gcloud CLI is required, but not installed.\n"
                "   Please follow the installation instructions at https://cloud.google.com/sdk/docs/install"
            ),
        )

    return mac_install_gcloud()
