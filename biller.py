#! /usr/bin/env python3

import click

from cli.people import cli as people_cli
from cli.provider import cli as provider_cli


@click.group()
def cli():
    pass


cli.add_command(people_cli, name='people')
cli.add_command(provider_cli, name='provider')

from biller import Providers
from biller import People
from biller.person import PersonType
from biller.charges import PaymentAmount
from biller.charges import ChargeType

@cli.command()
def dev():
    pro = Providers.load()
    peo = People.load()

    for person in peo:
        print("Person: {}".format(person.name))
        for provider in pro:
            print("\tService Provider: {}".format(provider.name))
            for bill in provider.bills:
                print("\t\tBill Due: {}".format(bill.payment_date))
                print("\t\tBill Charge: {}".format(bill.amount))
                days = set()
                for period in person.periods:
                    days |= bill.days & period.days
                print("\t\t\t{} days in house during this bill period".format(len(days)))

                print("\t\t\tBreakdown:")

                total_due = PaymentAmount(0)

                for charge in bill.charges:
                    if charge.type == ChargeType.STATIC:
                        if person.type == PersonType.TENANT:
                            share = charge.amount.split(peo.num_tenants)
                        else:
                            share = PaymentAmount(0)  # Non tenants are handled manually
                    elif charge.type == ChargeType.VARIABLE:
                        share = charge.amount.ratio(len(days), len(bill.days))  # Todo: Fix me
                    else:
                        raise Exception("Unknown Charge Type: {}".format(charge.type))
                    print("\t\t\t\t{}".format(charge.description))
                    print("\t\t\t\t\t Total: {}".format(charge.amount))
                    print("\t\t\t\t\t Share: {}".format(share))
                    total_due += share

                print("\t\t\tShare for this bill: {}".format(total_due))
if __name__ == "__main__":
    cli()
