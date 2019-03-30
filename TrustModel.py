#!/usr/bin/env python3

import sys
import argparse

import TrustManager

'''
A trust model simulation which uses machine learning techniques to find trust.

Author: Cody Lewis
Date: 2019-03-12
'''


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Simulate a trust model")
    PARSER.add_argument("--create-data", dest="is_creating",
                        action="store_const", const=True, default=False,
                        help="Create data and place it in the csv file.")
    PARSER.add_argument("-f", "--file", dest="filename",
                        action="store", default="reports.csv",
                        help="Specify the file to read from or write to.")
    ARGS = PARSER.parse_args()

    if len(sys.argv) == 1:
        PARSER.print_help()

    if ARGS.is_creating:
        TRUST_MANAGER = TrustManager.TrustManager()
        TRUST_MANAGER.bootstrap(500)
        TRUST_MANAGER.save_reports_csv(ARGS.filename)
