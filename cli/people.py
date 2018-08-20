import click

from biller import People

@click.group()
def people():
    pass


@people.command()
def list():
    p = People.load()
    click.echo("There are currently {} people.".format(len(p)))

    for person in p:
        click.echo("{0} - {1}".format(person.name, person.slug))