import os

from .io import YamlObject

class Account:

    def __init__(self, data, slug):
        self.data = data
        self.slug = slug

    @property
    def name(self):
        return self.data['name']


class AccountList(YamlObject):
    FILE = os.path.join(os.getcwd(), 'data', 'accounts.yml')

    @staticmethod
    def load():
        return AccountList(AccountList.FILE)

    def get_person(self, slug):

        return Person(self.data[slug], slug)

    def __iter__(self):
        self.position = -1  # Nasty Hack ALERT!
        return self

    def __next__(self):
        self.position += 1
        if self.position >= len(self.data.keys()):
            raise StopIteration
        slug = list(self.data.keys())[self.position]
        return Account(self.data[slug], slug)

    def __len__(self):
        return len(self.data.keys())