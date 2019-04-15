#!/usr/bin/env python3

import sys
import argparse

import TrustManager
import TrustManager.SVM

'''
A trust model simulation which uses machine learning techniques to find trust.

Author: Cody Lewis
Date: 2019-03-12
'''


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Simulate a trust model which uses either a kernel machine or neural network for trust management.")
    PARSER.add_argument("-c", "--create-data", dest="is_creating", action="store_const", const=True, default=False,
                        help="Create data and place it in the csv file.")
    PARSER.add_argument("-e", "--epochs", dest="epochs", type=int, action="store", default=200,
                        help="The number of epochs to bootstrap for.")
    PARSER.add_argument("-trf", "--train-file", dest="train_filename", action="store", default="reports-train.csv",
                        help="Specify the training data file to read from or write to.")
    PARSER.add_argument("-tef", "--test-file", dest="test_filename", action="store", default="reports-test.csv",
                        help="Specify the test file to read from or write to.")
    PARSER.add_argument("-s", "--svm", dest="use_svm", action="store_const", const=True, default=False,
                        help="Use a svm as the predicter")
    PARSER.add_argument("-a", "--ann", dest="use_ann", action="store_const", const=True, default=False,
                        help="Use an ann as the predicter")
    PARSER.add_argument("-t", "--train", dest="train", action="store_const", const=True, default=False,
                        help="Train the predicter on the previously generated data")
    PARSER.add_argument("-tra", "--transact", dest="transact", action="store", nargs=3, type=int,
                        metavar=("ID", "SERVICE", "CAPABILITY"),
                        help="Simulate a single transaction for node ID for SERVICE at CAPABILITY and print out the trusted list.")
    ARGS = PARSER.parse_args()

    if len(sys.argv) == 1:
        PARSER.print_help()

    TRUST_MANAGER = None

    if ARGS.is_creating:
        # First blank out file
        with open(ARGS.train_filename, "w") as FILE:
            FILE.write("")
        with open(ARGS.test_filename, "w") as FILE:
            FILE.write("")

        # Then create trust manager and bootstrap
        TRUST_MANAGER = TrustManager.TrustManager(
            train_filename=ARGS.train_filename, test_filename=ARGS.test_filename, use_svm=ARGS.use_svm
        )
        TRUST_MANAGER.bootstrap(ARGS.epochs)

    if ARGS.train:
        print("Training...")
        TRUST_MANAGER = TrustManager.load(ARGS.train_filename, ARGS.test_filename, ARGS.use_svm)
        TRUST_MANAGER.train()
        print("Done.")

    if ARGS.transact:
        TRUST_MANAGER = TrustManager.load(ARGS.train_filename, ARGS.test_filename, ARGS.use_svm)
        ID, SERVICE, CAP = ARGS.transact[0], ARGS.transact[1], ARGS.transact[2]
        print(f"Trusted list for node {ID} requesting service {SERVICE} at capability {CAP}")
        print()
        print(TRUST_MANAGER.find_best_servers(ID, SERVICE, CAP))
        TRUST_MANAGER.graph_recommendations(ID, SERVICE, CAP)

    if TRUST_MANAGER:
        TRUST_MANAGER.save()
