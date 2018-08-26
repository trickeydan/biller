import click

from biller.payment import PaymentAmount
from biller import Providers
from biller import People

@click.group(help='Manage bank account')
def cli():
    pass


@cli.command(help='Calculate bank account balance')
def balance():
    amount = PaymentAmount(0)
    providers = Providers.load()
    people = People.load()

    for provider in providers:
        for bill in provider.bills:
            if bill.paid:
                amount -= bill.amount

    for person in people:
        for payment in person.payments:
            amount += payment.amount
    click.echo("Balance: {}".format(amount))
