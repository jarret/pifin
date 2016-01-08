#!/usr/bin/python

import os
import sys
import datetime
from multiprocessing import Pool

from yahoo_finance import Currency as YFCurrency

# Set to True to output verbose blarbs for every pair that is queried
DEBUG = False

################################################################################
# additional methods for CurrencyPair class
################################################################################

class CurrencyPair(YFCurrency):
    def __init__(self, currencyNamePair):
        super(CurrencyPair, self).__init__("%s%s" % (currencyNamePair['base'],
                                                     currencyNamePair['quote']))
        self.base_currency = currencyNamePair['base']
        self.quote_currency = currencyNamePair['quote']

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
# report class
################################################################################

class CurrencyReport(object):
    def __init__(self, currencyNames):
        self.currencyNames = currencyNames
        self.currencyNamePairs = []
        for base_currency_name in self.currencyNames:
            for quote_currency_name in self.currencyNames:
                if base_currency_name != quote_currency_name:
                    currencyNamePair = {}
                    currencyNamePair['base'] = base_currency_name
                    currencyNamePair['quote'] = quote_currency_name
                    self.currencyNamePairs.append(currencyNamePair)
    def fetch(self):
        #use a process pool to send the queries in parallel
        pool = Pool(processes=len(self.currencyNamePairs))
        self.currencyPairs = pool.map(CurrencyPair, self.currencyNamePairs)

    def _get_currency_pair_rate(self, base_currency_name, quote_currency_name):
        for pair in self.currencyPairs:
            if pair.base_currency == base_currency_name and \
               pair.quote_currency == quote_currency_name:
                return pair.get_rate()
        return None

    def _rate_to_str(self, rate):
        return "%11.4f" % float(rate)

    def __str__(self):
        def horizontal_bar():
            bar = "---------"
            for currency in self.currencyNames:
                bar = bar + "-----------"
            return bar + "--\n"

        def base_line(base_currency_name):
            line = "| 1 %s |" % base_currency_name
            for quote_currency_name in self.currencyNames:
                if quote_currency_name == base_currency_name:
                    rate = 1.0
                else:
                    rate = self._get_currency_pair_rate(base_currency_name,
                                                        quote_currency_name)
                line = line + "%s" % self._rate_to_str(rate)
            return line + " |\n"

        def title_line():
            titleBar = "|       |"
            for currency in self.currencyNames:
                titleBar = titleBar + "%11s" % currency
            return titleBar + " |\n"

        string = ""
        string = string + "fetched at: %s\n" % datetime.datetime.now()
        string = string + horizontal_bar()
        string = string + title_line()
        string = string + horizontal_bar()
        for base_currency_name in self.currencyNames:
            string =  string + base_line(base_currency_name)
        string = string + horizontal_bar()
        return string

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

report = CurrencyReport(currencyNames)
report.fetch()
print report
