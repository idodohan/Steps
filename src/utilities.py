import time
from datetime import timedelta

# this file contains all sorts of utilities that are not linked to a specific model


def start_time_measure():
    return time.monotonic()


def end_time_measure(start_time: float):
    end_time = time.monotonic()
    return timedelta(milliseconds=end_time - start_time).microseconds / 1000
