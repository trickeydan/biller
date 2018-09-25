import enum
import os

from .io import YamlObject
from .payment import PaymentList
from .payment import PaymentAmount
from .period import PeriodList


class PersonType(enum.Enum):

    TENANT = 'Tenant'
    LONG_TERM_GUEST = 'LTG'


class Person:

    def __init__(self, data, slug):
        self.data = data
        self.slug = slug
        self.payment_list = None
        self.period_list = None

    @property
    def name(self):
        return self.data['preferred_name']

    @property
    def full_name(self):
        return self.data['full_name']

    @property
    def preferred_name(self):
        return self.data['preferred_name']

    @property
    def type(self):
        return PersonType(self.data['type'])

    @property
    def payments(self):
        if self.payment_list is None:
            self.payment_list = PaymentList.load(self.slug)
        return self.payment_list

    @property
    def periods(self):
        if self.period_list is None:
            self.period_list = PeriodList.load(self.slug)
        return self.period_list

    def get_balance(self):
        # Not implemented
        return PaymentAmount(0)

    def __str__(self):
        return self.name


class People(YamlObject):
    FILE = os.path.join(os.getcwd(), 'data', 'people.yml')

    @staticmethod
    def load():
        return People(People.FILE)

    def get_person(self, slug):

        return Person(self.data[slug], slug)

    @property
    def num_tenants(self):
        return 8  # Todo: FIX THIS

    def __iter__(self):
        self.position = -1  # Nasty Hack ALERT!
        return self

    def __next__(self):
        self.position += 1
        if self.position >= len(self.data.keys()):
            raise StopIteration
        slug = list(self.data.keys())[self.position]
        return Person(self.data[slug], slug)

    def __len__(self):
        return len(self.data.keys())