import click

from biller import Providers

p = Providers.load()


@click.group(help='Manage providers')
def cli():
    pass

@cli.command(help='List all providers')
def list():
    click.echo("There are currently {} providers.".format(len(p)))

    for provider in p:
        click.echo("{0} - {1}".format(provider.name, provider.slug))


@cli.command(help='View an individual provider')
@click.argument('slug')
def view(slug):
    provider = p.get_provider(slug)
    click.echo("Name: {}".format(provider.name))
    click.echo("Type: {}".format(provider.type))
