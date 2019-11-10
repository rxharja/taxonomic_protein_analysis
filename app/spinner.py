#!/usr/bin/env
import sys
import time
import threading

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor


    def __init__(self, out, delay=None):
        self.out = out
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay


    def spinner_task(self):
        spaces = "                                                          "
        while self.busy:
            sys.stdout.write(self.out + next(self.spinner_generator) + spaces)
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write("\r")
            sys.stdout.flush()


    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()


    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
