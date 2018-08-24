import click

from biller import Providers
from biller import People
from biller.person import PersonType
from biller.charges import PaymentAmount
from biller.charges import ChargeType

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


@cli.command(help='Calculate the latest bill for a person')
@click.argument('slug')
def bill(slug):
    pro = Providers.load()
    peo = People.load()

    person = peo.get_person(slug)

    print("# Person: {}".format(person.name))
    total_costs = PaymentAmount(0)
    for provider in pro:
        print("## Service Provider: {}".format(provider.name))
        bill_count = 0
        for bill in provider.bills:
            if not bill.informed:
                print("### Bill Due: {}\n".format(bill.payment_date))
                print("Bill Charge: {}\n".format(bill.amount))
            days = set()
            for period in person.periods:
                days |= bill.days & period.days
            if not bill.informed:
                print("{} days in house during this bill period\n".format(len(days)))
                print("#### Breakdown:")

            provider_total = PaymentAmount(0)

            for charge in bill.charges:
                if charge.type == ChargeType.STATIC:
                    if person.type == PersonType.TENANT:
                        share = charge.amount.split(peo.num_tenants)
                    else:
                        share = PaymentAmount(0)  # Non tenants are handled manually
                elif charge.type == ChargeType.VARIABLE:
                    share = charge.amount.ratio(len(days), bill.people_days)  # Todo: Fix me
                else:
                    raise Exception("Unknown Charge Type: {}".format(charge.type))
                if not bill.informed:
                    print("- {}".format(charge.description))
                    print("\t - Total: {}".format(charge.amount))
                    print("\t - Share: {}".format(share))
                provider_total += share

            if not bill.informed:
                print("\n**Share for this bill: {}**\n".format(provider_total))
            total_costs += provider_total
        if bill_count == 0:
            print("There are no bills for this provider.\n")

    print("## Summary\n")
    print("Total to pay: {}\n".format(total_costs))

    total_paid = PaymentAmount(0)

    for payment in person.payments:
        total_paid += payment.amount

    print("Total Paid: {}\n".format(total_paid))

    balance = total_paid - total_costs

    print("**Account Balance: {}**\n".format(balance))