"""Provides facilities for collecting metrics of each run of the program"""


import time
from lydoc import console


class Metrics(object):

    def __init__(self):
        self.start_time = time.time()
        self.elapsed = None

    def _time_snapshot(self):
        self.elapsed = time.time() - self.start_time

    def display(self):
        self._time_snapshot()
        console.display("Elapsed time {:.2f} seconds".format(
            self.elapsed))

