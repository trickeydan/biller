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

    for person in [peo.get_person('lead')]:
        print("# Person: {}".format(person.name))
        total_costs = PaymentAmount(0)
        for provider in pro:
            print("## Service Provider: {}".format(provider.name))
            if len(provider.bills) == 0:
                print("There are no bills for this provider.\n")
            for bill in provider.bills:
                print("### Bill Due: {}\n".format(bill.payment_date))
                print("Bill Charge: {}\n".format(bill.amount))
                days = set()
                for period in person.periods:
                    days |= bill.days & period.days
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
                    print("- {}".format(charge.description))
                    print("\t - Total: {}".format(charge.amount))
                    print("\t - Share: {}".format(share))
                    provider_total += share

                print("\n**Share for this bill: {}**\n".format(provider_total))
                total_costs += provider_total

        print("## Summary\n")
        print("Total to pay: {}\n".format(total_costs))

        total_paid = PaymentAmount(0)

        for payment in person.payments:
            total_paid += payment.amount

        print("Total Paid: {}\n".format(total_paid))

        balance = total_paid - total_costs

        print("**Account Balance: {}**\n".format(balance))
if __name__ == "__main__":
    cli()
