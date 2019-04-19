#!/usr/bin/env python3

import os
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
                        help="The number of epochs to bootstrap for. [default 200]")
    PARSER.add_argument("-s", "--svm", dest="use_svm", action="store_const", const=True, default=False,
                        help="Use a svm as the predictor")
    PARSER.add_argument("-a", "--ann", dest="use_ann", action="store_const", const=True, default=False,
                        help="Use an ann as the predictor [default predictor]")
    PARSER.add_argument("-t", "--train", dest="train", action="store_const", const=True, default=False,
                        help="Train the predictor on the previously generated data")
    PARSER.add_argument("-co", "--continue", dest="cont", action="store_const", const=True, default=False,
                        help="Continue training the ann.")
    PARSER.add_argument("-tr", "--transact", dest="transact", action="store", nargs=3, type=int,
                        metavar=("ID", "SERVICE", "CAPABILITY"),
                        help="Simulate a single transaction for node ID for SERVICE at CAPABILITY and print out the trusted list.")
    PARSER.add_argument("-si", "--simulate", dest="simulate", action="store_const", const=True, default=False,
                        help="Simulate EPOCH number of transactions and find the number of bad, okay, and good transactions that occured.")
    PARSER.add_argument("-tp", "--time-predict", dest="time_predict", action="store_const", const=True, default=False,
                        help="Find the average time it takes for the trust manager to make a prediction.")
    ARGS = PARSER.parse_args()

    if not os.path.exists("data"):
        os.makedirs("data")
    TRAIN_FILENAME = "data/reports-train.csv"
    TEST_FILENAME = "data/reports-test.csv"

    if len(sys.argv) == 1:
        # First blank out file
        with open(TRAIN_FILENAME, "w") as FILE:
            FILE.write("")
        with open(TEST_FILENAME, "w") as FILE:
            FILE.write("")

        # Then create trust manager and bootstrap
        TRUST_MANAGER = TrustManager.TrustManager(
            train_filename=TRAIN_FILENAME, test_filename=TEST_FILENAME, use_svm=ARGS.use_svm
        )
        TRUST_MANAGER.bootstrap(ARGS.epochs)
        TRUST_MANAGER.train(ARGS.cont)
        TRUST_MANAGER.graph_recommendations(1, 1, 1)
        BAD_PER, OK_PER, GOOD_PER = TRUST_MANAGER.simulate_transactions(ARGS.epochs)
        print(f"Percentage of bad transactions: {BAD_PER}")
        print(f"Percentage of okay transactions: {OK_PER}")
        print(f"Percentage of good transactions: {GOOD_PER}")

    TRUST_MANAGER = None

    if ARGS.is_creating:
        # First blank out file
        with open(TRAIN_FILENAME, "w") as FILE:
            FILE.write("")
        with open(TEST_FILENAME, "w") as FILE:
            FILE.write("")

        # Then create trust manager and bootstrap
        TRUST_MANAGER = TrustManager.TrustManager(
            train_filename=TRAIN_FILENAME, test_filename=TEST_FILENAME, use_svm=ARGS.use_svm
        )
        TRUST_MANAGER.bootstrap(ARGS.epochs)

    if ARGS.train:
        print("Training...")
        TRUST_MANAGER = TrustManager.load(TRAIN_FILENAME, TEST_FILENAME, ARGS.use_svm)
        TRUST_MANAGER.train(ARGS.cont)

    if ARGS.transact:
        TRUST_MANAGER = TrustManager.load(TRAIN_FILENAME, TEST_FILENAME, ARGS.use_svm)
        ID, SERVICE, CAP = ARGS.transact[0], ARGS.transact[1], ARGS.transact[2]
        print(f"Trusted list for node {ID} requesting service {SERVICE} at capability {CAP}")
        print()
        print(TRUST_MANAGER.find_best_servers(ID, SERVICE, CAP))
        TRUST_MANAGER.graph_recommendations(ID, SERVICE, CAP)

    if ARGS.simulate:
        TRUST_MANAGER = TrustManager.load(TRAIN_FILENAME, TEST_FILENAME, ARGS.use_svm)
        BAD_PER, OK_PER, GOOD_PER = TRUST_MANAGER.simulate_transactions(ARGS.epochs)
        print(f"Percentage of bad transactions: {BAD_PER}%")
        print(f"Percentage of okay transactions: {OK_PER}%")
        print(f"Percentage of good transactions: {GOOD_PER}%")

    if ARGS.time_predict:
        TRUST_MANAGER = TrustManager.load(TRAIN_FILENAME, TEST_FILENAME, ARGS.use_svm)
        print(f"Average time to predict is {TRUST_MANAGER.time_predict()} seconds")

    if TRUST_MANAGER:
        TRUST_MANAGER.save()
        print("Done.")
