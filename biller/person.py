import enum
import os

from .io import YamlObject
from .payment import PaymentList


class PersonType(enum.Enum):

    TENANT = 'Tenant'
    LONG_TERM_GUEST = 'LTG'


class Person:

    def __init__(self, data, slug):
        self.data = data
        self.slug = slug
        self.payment_list = None

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


class People(YamlObject):
    FILE = os.path.join(os.getcwd(), 'data', 'people.yml')

    @staticmethod
    def load():
        return People(People.FILE)

    def get_person(self, slug):

        return Person(self.data[slug], slug)