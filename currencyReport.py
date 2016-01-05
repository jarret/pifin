#!/usr/bin/python

import os
import sys
import datetime

from yahoo_finance import Currency as YFCurrency

# Set to True to output verbose blarbs for every pair that is queried
DEBUG = False

################################################################################
# additional methods for CurrencyPair class
################################################################################

class CurrencyPair(YFCurrency):
    def __init__(self, base, quote):
        super(CurrencyPair, self).__init__("%s%s" % (base, quote))
        self.base_currency = base
        self.quote_currency = quote

    def _print_data(self, data):
        for label, val in data.items():
            print "%s %s" % (label, val)

    def _fetch(self):
        fetchedData = super(CurrencyPair, self)._fetch()
        if DEBUG:
            self._print_data(fetchedData)
        return fetchedData

    def get_id(self):
        return self.data_set['id']

################################################################################
# deal with input currency file
################################################################################

usage = "USAGE = ./currencyReport.py <currencyFile>"

if not len(sys.argv) == 2:
    sys.exit(usage)

currencyFile = sys.argv[1]

if not os.path.isfile(currencyFile):
    sys.exit("no such file: %s\n" % currencyFile)

currencyFile = os.path.abspath(currencyFile)

currencies = []
for line in open(currencyFile).readlines():
    currency = line.rstrip()
    currencies.append(currency)

################################################################################
# format particular strings
################################################################################

def rate_to_str(rate):
    return "%11.4f" % float(rate)

################################################################################
# generate report
################################################################################

def print_horizontal_bar():
    bar = "---------"
    for currency in currencies:
        bar = bar + "-----------"
    print bar + "--"

def print_base_line(base):
    line = "| 1 %s |" % base
    for quote in currencies:
        if quote == base:
            rate = 1.0
        else:
            rate = CurrencyPair(base, quote).get_rate()
        line = line + "%s" % rate_to_str(rate)
    print line + " |"

def print_title_line():
    titleBar = "|       |"
    for currency in currencies:
        titleBar = titleBar + "%11s" % currency
    print titleBar + " |"

print "fetched at: %s" % datetime.datetime.now()
print_horizontal_bar()
print_title_line()
print_horizontal_bar()
for base in currencies:
    print_base_line(base)
print_horizontal_bar()
