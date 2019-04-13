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
    PARSER.add_argument("-e", "--epochs", dest="epochs",
                        action="store", default="200",
                        help="The number of epochs to bootstrap for.")
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
    PARSER.add_argument("--train-ann", dest="train_ann", action="store_const",
                        const=True, default=False,
                        help="Train an ANN on the previously generated data")
    ARGS = PARSER.parse_args()

    if len(sys.argv) == 1:
        PARSER.print_help()

    if ARGS.is_creating:
        # First blank out file
        with open(ARGS.train_filename, "w") as FILE:
            FILE.write("")
        with open(ARGS.test_filename, "w") as FILE:
            FILE.write("")

        # Then create trust manager and bootstrap
        TRUST_MANAGER = TrustManager.TrustManager(
            train_filename=ARGS.train_filename, test_filename=ARGS.test_filename
        )
        TRUST_MANAGER.bootstrap(int(ARGS.epochs))
        joblib.dump(TRUST_MANAGER, "trust_manager.pkl")

    if ARGS.evolve_svm:
        print("Evolving...")
        TRUST_MANAGER = joblib.load("trust_manager.pkl")
        TRUST_MANAGER.set_filenames(ARGS.train_filename, ARGS.test_filename)
        TRUST_MANAGER.evolve_svm()
        print("Done. Parameters written to svm_params.csv")

    if ARGS.fit_svm:
        TRUST_MANAGER = TrustManager.TrustManager(
            train_filename=ARGS.train_filename, test_filename=ARGS.test_filename
        )
        print("Fitting SVM...")
        SVM = TRUST_MANAGER.train_svm()
        print("SVM fitted")
        joblib.dump(SVM, "svm.pkl")
        print("Done. SVM saved as svm.pkl")

    if ARGS.train_ann:
        print("Training...")
        TRUST_MANAGER = joblib.load("trust_manager.pkl")
        TRUST_MANAGER.set_filenames(ARGS.train_filename, ARGS.test_filename)
        TRUST_MANAGER.train_ann()
        print("Done.")
