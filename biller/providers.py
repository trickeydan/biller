import os

from .io import YamlObject


class Provider:

    def __init__(self, data, slug):
        self.data = data
        self.slug = slug

    @property
    def name(self):
        return self.data['name']

    @property
    def type(self):
        return self.data['type']


class Providers(YamlObject):
    FILE = os.path.join(os.getcwd(), 'data', 'providers.yml')

    @staticmethod
    def load():
        return Providers(__class__.FILE)

    def get_provider(self, slug):
        return Provider(self.data[slug], slug)