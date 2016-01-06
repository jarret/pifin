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
    def __init__(self, base_currency_name, quote_currency_name):
        super(CurrencyPair, self).__init__("%s%s" % (base_currency_name,
                                                     quote_currency_name))
        self.base_currency = base_currency_name
        self.quote_currency = quote_currency_name

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

currencyNames = []
for line in open(currencyFile).readlines():
    currencyName = line.rstrip()
    currencyNames.append(currencyName)

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
    for currency in currencyNames:
        bar = bar + "-----------"
    print bar + "--"

def print_base_line(base_currency_name):
    line = "| 1 %s |" % base_currency_name
    for quote_curency_name in currencyNames:
        if quote_curency_name == base_currency_name:
            rate = 1.0
        else:
            rate = CurrencyPair(base_currency_name,
                                quote_curency_name).get_rate()
        line = line + "%s" % rate_to_str(rate)
    print line + " |"

def print_title_line():
    titleBar = "|       |"
    for currency in currencyNames:
        titleBar = titleBar + "%11s" % currency
    print titleBar + " |"

print "fetched at: %s" % datetime.datetime.now()
print_horizontal_bar()
print_title_line()
print_horizontal_bar()
for base_currency_name in currencyNames:
    print_base_line(base_currency_name)
print_horizontal_bar()
