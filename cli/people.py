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


@cli.command(help='Calculate the latest bill for a person')
@click.argument('slug')
def bill(slug):
    pro = Providers.load()
    peo = People.load()

    person = peo.get_person(slug)

    print("# Person: {}".format(person.name))
    total_costs = PaymentAmount(0)
    for provider in pro:

        bill_count = 0

        for bill in provider.bills:
            if not bill.is_transfer():
                if not bill.informed:
                    bill_count += 1
        if bill_count > 0:
            print("## Service Provider: {}".format(provider.name))
        bill_count = 0
        
        for bill in provider.bills:
            if not bill.is_transfer():
                if not bill.informed:
                    bill_count += 1
                    if "payment_date" in bill.data:
                        print("### Bill Payment Date: {}\n".format(bill.payment_date))
                    else:
                        print("### Bill Payment Date: Not Yet Known")
                    print("Bill Charge: {}\n".format(bill.amount))
                days = set()
                for period in person.periods:
                    days |= bill.days & period.days
                if not bill.informed:
                    if len(days) > 0 and charge.type != ChargeType.STATIC:
                        print("{} days in house during this bill period.\n".format(len(days)))
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

    print("## Summary\n")


    total_paid = PaymentAmount(0)

    for payment in person.payments:
        total_paid += payment.amount

    print("You have paid {} into the account so far, out of {}.\n".format(total_paid,total_costs))

    bal = total_paid - total_costs

    print("**Your Balance: {}**\n".format(bal))

    if bal.is_negative():
        print("You will need to pay at least {}".format(abs(bal)))

@cli.command(help='Calculate the balance for a person')
@click.argument('slug')
def balance(slug):
    pro = Providers.load()
    peo = People.load()

    person = peo.get_person(slug)

    total_costs = PaymentAmount(0)
    for provider in pro:
        for bill in provider.bills:
            if not bill.is_transfer():
                days = set()
                for period in person.periods:
                    days |= bill.days & period.days
                
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
                    provider_total += share

                total_costs += provider_total

    total_paid = PaymentAmount(0)

    for payment in person.payments:
        total_paid += payment.amount

    balance = total_paid - total_costs

    print("{}: {}".format(person.name, balance))

@cli.command(help='Summarise all people')
@click.pass_context
def summary(ctx):

    peo = People.load()

    for person in peo:
        ctx.invoke(balance, slug=person.slug)