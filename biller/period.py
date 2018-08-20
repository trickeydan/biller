import os

from .io import YamlObject


class Period:

    def __init__(self, data):
        self.data = data

    @property
    def start_date(self):
        return self.data['start_date']

    @property
    def end_date(self):
        return self.data['end_date']

    @property
    def ongoing(self):
        return self.end_date is None


class PeriodList(YamlObject):

    @staticmethod
    def load(slug):
        return PeriodList(os.path.join(os.getcwd(), 'data', 'residency', '{}.yml'.format(slug)))

    def __iter__(self):
        self.position = -1  # Nasty Hack ALERT!
        return self

    def __next__(self):
        self.position += 1
        if self.position >= len(self.data):
            raise StopIteration
        return Period(self.data[self.position])