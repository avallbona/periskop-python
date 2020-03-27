from periskop.collector import ExceptionCollector
from periskop.exporter import ExceptionExporter

ec = ExceptionCollector()


def foo():
    try:
        l = []
        l[1] = 2
    except Exception as exception:
        ec.report(exception)

foo()

ee = ExceptionExporter(ec)
print(ee.export())
