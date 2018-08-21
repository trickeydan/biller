import os

from .io import YamlObject
import datetime


class Period:

    def __init__(self, data):
        self.data = data
        self.days_set = None

    @property
    def start_date(self):
        return self.data['start_date']

    @property
    def end_date(self):
        return self.data['end_date']

    @property
    def ongoing(self):
        return self.end_date is None

    @property
    def days(self):
        if self.end_date is None:
            end = datetime.datetime.now().date()
        else:
            end = self.end_date
        if self.days_set is None:
            self.days_set = set([
                self.start_date + datetime.timedelta(days=x) for x in range(0, (end - self.start_date).days)
            ])
            self.days_set.add(end)
        return self.days_set


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