#!/usr/bin/python

import os
import sys
import datetime
from multiprocessing import Pool

from yahoo_finance import Share as YFShare

# Set to True to output verbose blarbs for every share that is queried
DEBUG = False

################################################################################
# additional methods for Share class
################################################################################

class Share(YFShare):
    def get_symbol(self):
        return self.data_set['Symbol']

    def get_name(self):
        return self.data_set['Name']

    def get_currency(self):
        return self.data_set['Currency']

    def get_percent_change(self):
        return self.data_set['PercentChange']

    def _print_data(self, data):
        for label, val in data.items():
            print "%s %s" % (label, val)
        print ""

    def _fetch(self):
        fetchedData = super(Share, self)._fetch()
        if DEBUG:
            self._print_data(fetchedData)
        return fetchedData

################################################################################
# report class
################################################################################

class DayReport(object):
    def __init__(self, symbols):
        self.symbols = symbols
        # terminal colors
        self.BLUE = '\033[94m'
        self.GREEN = '\033[92m'
        self.RED = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def fetch(self):
        # use a process pool to send the queries in parallel
        pool = Pool(processes=len(self.symbols))
        self.shares = pool.map(Share, self.symbols)

    def _greenify(self, string):
        return self.GREEN + string + self.ENDC

    def _redify(self, string):
        return self.RED + string + self.ENDC

    def _boldify(self, string):
        return self.BOLD + string + self.ENDC

    def _price_to_str(self, price):
        return "%8s" % ("%.2f" % price)

    def _name_to_str(self, name):
        return "%-20s" % name[:20]

    def _percent_change_to_str(self, percent_change):
        isNegative = (percent_change[0] == '-')
        val = float(percent_change[1:-1])
        isZero = (val == 0.0)
        valstr = "%6.2f" % val
        if isNegative:
            return self._redify(valstr)
        if isZero:
            return valstr
        return self._greenify(valstr)

    def _symbol_to_str(self, symbol):
        return self._boldify("%-10s" % symbol)

    def __str__(self):
        string = ""
        if (self.shares == None):
            return "(not fetched)"
        string = string + "fetched at: %s\n" % datetime.datetime.now()
        string = string + \
            "SYMBOL     NAME                       PRICE   %CHNG\n"
        string = string + \
            "---------------------------------------------------\n"
        for share in self.shares:
            name = share.get_name()
            price = float(share.get_price())
            currency = share.get_currency()
            percent_change = share.get_percent_change()
            symbol = share.get_symbol()
            string = string + "%s %s %s %s %s\n" % (self._symbol_to_str(symbol),
                                                  self._name_to_str(name),
                                                  self._price_to_str(price),
                                                  currency,
                                    self._percent_change_to_str(percent_change))
        return string


################################################################################
# main execution
################################################################################

usage = "USAGE = ./dayReport.py <symbolFile>"

if not len(sys.argv) == 2:
    sys.exit(usage)

symbolFile = sys.argv[1]

if not os.path.isfile(symbolFile):
    sys.exit("no such file: %s\n" % symbolFile)

symbolFile = os.path.abspath(symbolFile)

inputSymbols = []
for inputLine in open(symbolFile).readlines():
    symbol = inputLine.rstrip()
    inputSymbols.append(symbol)
report = DayReport(inputSymbols)
report.fetch()
print report
