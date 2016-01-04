# pifin

A simple set of console-based tools for tracking finance data. It queries yahoo finance for its data using the yahoo-finance package (which is a prerequisite).

$ pip install yahoo-finance

## dayReport.py

This tool takes a list of stock symbols in a file. Each stock is outputted with a price and a daily percent change. Change will be shown as green if positive, and red if negative.

Example:
![alt text](https://github.com/jarret/pifin/dayReportExample.png "dayReport")
