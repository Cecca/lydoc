"""Provides facilities for collecting metrics of each run of the program"""

# For Python 2/3 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals


import time
from lydoc import console
import logging


class Metrics(object):

    def __init__(self):
        self.start_time = time.time()
        self.elapsed = None
        self.files = 0
        self.lines = 0
        self.errors = 0

    def _time_snapshot(self):
        self.elapsed = time.time() - self.start_time

    def display(self):
        self._time_snapshot()
        console.display(
            ("time {:.2f} seconds {} "
             "files, {} lines, {:.2f} lines/sec - "
             "{} errors").format(
                 self.elapsed, self.files, self.lines,
                 self.lines / self.elapsed,
                 self.errors))

    def record_file(self, file_text):
        self.files += 1
        self.lines += file_text.count('\n') + 1

    def record_error(self, error):
        self.errors += 1
