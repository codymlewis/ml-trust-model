#!/usr/bin/env python3

import sys
import argparse

import joblib

import TrustManager
import TrustManager.SVM

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
    PARSER.add_argument("-trf", "--train-file", dest="train_filename",
                        action="store", default="reports-train.csv",
                        help="Specify the training data file to read from or write to.")
    PARSER.add_argument("-tef", "--test-file", dest="test_filename",
                        action="store", default="reports-test.csv",
                        help="Specify the test file to read from or write to.")
    PARSER.add_argument("--fit-svm", dest="fit_svm", action="store_const",
                        const=True, default=False,
                        help="Train an SVM on previously generated data and test on a new network.")
    PARSER.add_argument("--evolve-svm", dest="evolve_svm", action="store_const",
                        const=True, default=False,
                        help="Perform an evolutionary algorithm to find the optimal values for C and gamma")
    ARGS = PARSER.parse_args()

    if len(sys.argv) == 1:
        PARSER.print_help()

    if ARGS.is_creating:
        # First blank out file
        with open(ARGS.filename, "w") as FILE:
            FILE.write("")

        # Then create trust manager and bootstrap
        TRUST_MANAGER = TrustManager.TrustManager(filename=ARGS.filename)
        TRUST_MANAGER.bootstrap(1)
        joblib.dump(TRUST_MANAGER, "trust_manager.pkl")

    if ARGS.evolve_svm:
        print("Evolving...")
        TRUST_MANAGER = joblib.load("trust_manager.pkl")
        TRUST_MANAGER.set_filename(ARGS.filename)
        print(TRUST_MANAGER.evolve_svm())

    if ARGS.fit_svm:
        TRUST_MANAGER = TrustManager.TrustManager(filename=ARGS.filename)
        print("Fitting SVM...")
        SVM = TRUST_MANAGER.train_svm()
        print("SVM fitted")
        joblib.dump(SVM, "svm.pkl")
        print("Done. SVM saved as svm.pkl")
