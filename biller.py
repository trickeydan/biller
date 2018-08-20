#! /usr/bin/env python3

import click

from cli.people import people

@click.group()
def cli():
    pass

cli.add_command(people)





if __name__ == "__main__":
    cli()