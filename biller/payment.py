import os
import math

from .io import YamlObject


class PaymentAmount:

    def __init__(self, raw_pence):
        self.raw_pence = raw_pence

    @property
    def pence(self):
        return math.ceil(self.raw_pence)

    @property
    def pounds(self):
        return round(self.pence / 100, 2)

    def __str__(self):
        return "£{}".format(self.pounds)

    def __add__(self, other):
        return PaymentAmount(self.raw_pence + other.raw_pence)

    def __iadd__(self, other):
        self.raw_pence += other.raw_pence
        return self

    def split(self, number):
        return PaymentAmount(self.raw_pence / number)

    def ratio(self, present, total):
        return PaymentAmount(self.raw_pence * present / total)


class Payment:

    def __init__(self, data):
        self.data = data

    @property
    def date(self):
        return self.data['date']

    @property
    def amount(self):
        return PaymentAmount(self.data['amount'])


class PaymentList(YamlObject):

    @staticmethod
    def load(slug):
        return PaymentList(os.path.join(os.getcwd(), 'data', 'payments', '{}.yml'.format(slug)))

    def __iter__(self):
        self.position = -1  # Nasty Hack ALERT!
        return self

    def __next__(self):
        self.position += 1
        if self.position >= len(self.data):
            raise StopIteration
        return Payment(self.data[self.position])
