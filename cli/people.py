import click

from biller import People

p = People.load()


@click.group(help='Manage people')
def cli():
    pass


@cli.command(help='List all people')
def list():
    click.echo("There are currently {} people.".format(len(p)))

    for person in p:
        click.echo("{0} - {1}".format(person.name, person.slug))


@cli.command(help='View an individual person')
@click.argument('slug')
def view(slug):
    person = p.get_person(slug)
    click.echo("Full Name: {}".format(person.full_name))
    click.echo("Preferred Name: {}".format(person.preferred_name))
    click.echo("Preferred Name: {}".format(person.preferred_name))
    click.echo("Type: {}".format(person.type))
    click.echo("Balance: {}".format(person.get_balance()))