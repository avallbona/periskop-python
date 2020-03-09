import sys

from collector import ExceptionCollector

ec = ExceptionCollector()


def foo():
    try:
        l = []
        l[1] = 2
    except Exception as exception:
        ec.add_exception(exception)

foo()
