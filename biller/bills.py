import os
import datetime

from .io import YamlObject
from .payment import PaymentAmount
from .charges import ChargeList


class Bill:

    def __init__(self, data):
        self.data = data
        self.days_set = None

    @property
    def payment_date(self):
        return self.data['payment_date']

    @property
    def period_start(self):
        return self.data['period_start']

    @property
    def period_end(self):
        return self.data['period_end']

    @property
    def amount(self):
        return PaymentAmount(self.data['amount'])

    @property
    def charges(self):
        return ChargeList(self.data['charges'])

    @property
    def days(self):
        if self.days_set is None:
            self.days_set = set([self.period_start + datetime.timedelta(days=x) for x in range(0, (self.period_end-self.period_start).days)])
            self.days_set.add(self.period_end)
        return self.days_set


class BillList(YamlObject):

    @staticmethod
    def load(slug):
        return BillList(os.path.join(os.getcwd(), 'data', 'bills', '{}.yml'.format(slug)))

    def __iter__(self):
        self.position = -1  # Nasty Hack ALERT!
        return self

    def __next__(self):
        self.position += 1
        if self.data is None or self.position >= len(self.data):
            raise StopIteration
        return Bill(self.data[self.position])