import click

from biller.payment import PaymentAmount
from biller import Providers
from biller import People
from biller import AccountList

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

class Transaction:

    def __init__(self, date, to, fro, amount):
        self.date = date
        self.to = to
        self.fro = fro
        self.amount = amount

@cli.command(help='List all transactions')
def transactions():

    providers = Providers.load()
    accounts = AccountList.load()
    people = People.load()

    transactions = []

    for provider in providers:
        for bill in provider.bills:
            if "payment_date" in bill.data:
                if bill.is_transfer():
                    t = Transaction(bill.payment_date, bill.transfer_to(), bill.transfer_from(),bill.amount)
                else:
                    t = Transaction(bill.payment_date, provider, bill.account , bill.amount)
                transactions.append(t)
    
    for person in people:
        for payment in person.payments:
            t = Transaction(payment.date, payment.account, person, payment.amount)
            transactions.append(t)
    
    
    
    
    transactions.sort(key= lambda r: r.date)

    for t in transactions:
        print(t.date, t.fro, t.to, t.amount)