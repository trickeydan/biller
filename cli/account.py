import click

from biller.payment import PaymentAmount
from biller import Providers
from biller import People

@click.group(help='Manage accounts')
def cli():
    pass


@cli.command(help='Calculate account balance')
@click.argument('slug')
def balance(slug):
    amount = PaymentAmount(0)
    providers = Providers.load()
    people = People.load()

    for provider in providers:
        for bill in provider.bills:
            if bill.is_transfer():
                if bill.transfer_to() == slug:
                    amount += bill.amount
                if bill.transfer_from() == slug:
                    amount -= bill.amount
            else:
                if bill.paid and bill.account == slug:
                    amount -= bill.amount

    for person in people:
        for payment in person.payments:
            if bill.account == slug:
                amount += payment.amount
    click.echo("Balance: {}".format(amount))
