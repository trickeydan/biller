#! /usr/bin/env python3

import click

from cli.people import cli as people_cli
from cli.provider import cli as provider_cli
from cli.account import cli as account_cli


@click.group()
def cli():
    pass


cli.add_command(people_cli, name='people')
cli.add_command(provider_cli, name='provider')
cli.add_command(account_cli, name='account')


if __name__ == "__main__":
    cli()
