# SPDX-FileCopyrightText: 2023-present Julien Kieffer <julien@mefa.tech>
#
# SPDX-License-Identifier: BSD-3-Clause
import click

from docker_craft.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="docker-craft")
def docker_craft():
    click.echo("Hello world!")
