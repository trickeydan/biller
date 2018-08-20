import os

from .io import YamlObject
from .bills import BillList


class Provider:

    def __init__(self, data, slug):
        self.data = data
        self.slug = slug
        self.bill_list = None

    @property
    def name(self):
        return self.data['name']

    @property
    def type(self):
        return self.data['type']

    @property
    def bills(self):
        if self.bill_list is None:
            self.bill_list = BillList.load(self.slug)
        return self.bill_list


class Providers(YamlObject):
    FILE = os.path.join(os.getcwd(), 'data', 'providers.yml')

    @staticmethod
    def load():
        return Providers(__class__.FILE)

    def get_provider(self, slug):
        return Provider(self.data[slug], slug)

    def __iter__(self):
        self.position = -1  # Nasty Hack ALERT!
        return self

    def __next__(self):
        self.position += 1
        if self.position >= len(self.data.keys()):
            raise StopIteration
        slug = list(self.data.keys())[self.position]
        return Provider(self.data[slug], slug)

    def __len__(self):
        return len(self.data.keys())