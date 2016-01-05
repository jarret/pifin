# pifin

A simple set of console-based tools for tracking finance data. It queries yahoo finance for its data using the yahoo-finance package (which is a prerequisite).

$ pip install yahoo-finance

## dayReport.py

This tool takes a list of stock symbols in a file. Each stock is outputted with a price and a daily percent change. Change will be shown as green if positive, and red if negative.

Example:

![alt text][dayReportExample]

[dayReportExample]: https://github.com/jarret/pifin/blob/master/dayReportExample.png "DayReportExample"

## currencyReport.py

This tool takes a list of currency symbols (USD, CAD, etc.) in a file. A matrix of the exchange rate of each currency paired with every other currency in the list is outputted.
