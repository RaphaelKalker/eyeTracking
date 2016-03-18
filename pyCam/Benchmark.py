import logging
import time

__author__ = 'Raphael'

class Benchmark:

    def __init__(self, benchmarkName):
        self.log = logging.getLogger(__name__)
        self.benchmarkName = benchmarkName
        self.__start__()

    def __start__(self):
        self.startTime = time.time()

    def end(self):
        self.endTime = time.time()
        self.log.debug(self.benchmarkName + " -> {}s".format("%.2f" % (self.endTime - self.startTime)))
        self.__start__()
