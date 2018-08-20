import enum

from .payment import PaymentAmount


class ChargeType(enum.Enum):

    STATIC = 'static'
    VARIABLE = 'variable'


class Charge:

    def __init__(self, data):
        self.data = data

    @property
    def description(self):
        return self.data['description']

    @property
    def type(self):
        return ChargeType(self.data['type'])

    @property
    def amount(self):  # The total amount

        if 'cost' in self.data:
            return PaymentAmount(self.data['cost'])

        if 'unit_cost' in self.data and 'unit_amount' in self.data:
            return PaymentAmount(self.data['unit_cost'] * self.data['unit_amount'])
        raise ValueError('Bad Cost info on Charge')


class ChargeList:

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        self.position = -1  # Nasty Hack ALERT!
        return self

    def __next__(self):
        self.position += 1
        if self.position >= len(self.data):
            raise StopIteration
        return Charge(self.data[self.position])