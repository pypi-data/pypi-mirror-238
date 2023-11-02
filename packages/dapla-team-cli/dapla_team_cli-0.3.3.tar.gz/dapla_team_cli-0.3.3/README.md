# Dapla Team CLI

[![PyPI](https://img.shields.io/pypi/v/dapla-team-cli.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/dapla-team-cli.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/dapla-team-cli)][python version]
[![License](https://img.shields.io/pypi/l/dapla-team-cli)][license]

[![Tests](https://github.com/statisticsnorway/dapla-team-cli/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/statisticsnorway/dapla-team-cli/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/dapla-team-cli/
[status]: https://pypi.org/project/dapla-team-cli/
[python version]: https://pypi.org/project/dapla-team-cli
[tests]: https://github.com/statisticsnorway/dapla-team-cli/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/statisticsnorway/dapla-team-cli
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

A CLI for working with Dapla teams.

![dpteam --help](docs/dapla-team-cli-help.png)
![IAM Bindings](docs/iam-bindings.gif)

For [installation options see below](#installation), for usage instructions
[see the manual](https://statisticsnorway.github.io/dapla-team-cli/) or type `--help` on the command line.

<!-- this anchor is linked to, so avoid renaming it -->

## Installation

Install with [pipx]:

```console
pipx install dapla-team-cli
```

(Be patient, installation can take some time.)

## Features

- Assign bucket access and GCP roles to members for a limited amount of time
- Get an overview of a team's groups and members
- Make instant changes to your team's access groups, e.g. add a new team member to your team's "developers" group.
- Register team secrets (in a team's GCP Secret Manager service)
- Diagnose your system and get help to install required tooling for easy setup of your development environment

## Links

- [PyPI]

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Dapla Team CLI_ is free and open source software.

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[pypi]: https://pypi.org/project/dapla-team-cli/
[file an issue]: https://github.com/statisticsnorway/dapla-team-cli/issues
[pipx]: https://pypa.github.io/pipx

<!-- github-only -->

[license]: https://github.com/statisticsnorway/dapla-team-cli/blob/main/LICENSE
[contributor guide]: https://github.com/statisticsnorway/dapla-team-cli/blob/main/CONTRIBUTING.md
[command-line reference]: https://statisticsnorway.github.io/dapla-team-cli/command_reference/
