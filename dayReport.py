#!/usr/bin/python

import os
import sys
import datetime

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
# deal with input symbol file
################################################################################

usage = "USAGE = ./dayReport.py <symbolFile>"

if not len(sys.argv) == 2:
    sys.exit(usage)

symbolFile = sys.argv[1]

if not os.path.isfile(symbolFile):
    sys.exit("no such file: %s\n" % symbolFile)

symbolFile = os.path.abspath(symbolFile)

################################################################################
# query Yahoo for the information each symbol
################################################################################

refs = []
for line in open(symbolFile).readlines():
    symbol = line.rstrip()
    ref = Share(symbol)
    refs.append(ref)

################################################################################
# utilities
################################################################################

# terminal colors
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def greenify(string):
    return GREEN + string + ENDC

def redify(string):
    return RED + string + ENDC

################################################################################
# format particular strings
################################################################################

def price_to_str(price):
    return "%8s" % ("%.2f" % price)

def name_to_str(name):
    return "%-20s" % name[:20]

def percent_change_to_str(percent_change):
    isNegative = (percent_change[0] == '-')
    val = float(percent_change[1:-1])
    isZero = (val == 0.0)
    valstr = "%6.2f" % val
    if isNegative:
        return redify(valstr)
    if isZero:
        return valstr
    return greenify(valstr)

def symbol_to_str(symbol):
    return "%-10s" % symbol

################################################################################
# output table
################################################################################

print "fetched at: %s" % datetime.datetime.now()
print "SYMBOL     NAME                       PRICE   %CHNG"
print "---------------------------------------------------"
for ref in refs:
    name = ref.get_name()
    price = float(ref.get_price())
    currency = ref.get_currency()
    percent_change = ref.get_percent_change()
    symbol = ref.get_symbol()
    print "%s %s %s %s %s" % (symbol_to_str(symbol), name_to_str(name),
                              price_to_str(price), currency,
                              percent_change_to_str(percent_change))
