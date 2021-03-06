import timeit
import numpy as np

'''
A few utility functions.

Author: Cody Lewis
Date: 2019-03-30
'''


def print_progress(current_epoch, total_epochs, progress_len=31, prefix=""):
    '''
    Print a progress bar about how far a process has went through it's epochs.
    '''
    progress = int(100 * current_epoch / total_epochs)

    if (100 * current_epoch / total_epochs) == progress:
        progress_bar_progress = int(progress_len * progress * 0.01)
        if progress_bar_progress != 0:
            unprogressed = progress_len - progress_bar_progress
        else:
            unprogressed = progress_len - 1
        progress_bar = "["
        progress_bar += "".join(
            ["=" for _ in range(progress_bar_progress - 2)] + [">" if unprogressed > 0 else "="]
        )
        progress_bar += "".join(["." for _ in range(unprogressed)])
        progress_bar += "]"
        print(f"\r{prefix} {progress_bar} {progress}%", end="\r")


def wrong_note(note):
    '''
    Get the wrong note randomly
    '''
    wrong_notes = {-1, 0, 1} - {note}
    return list(wrong_notes)[int(np.round(np.random.rand()))]


def get_conditioned_ids(no_of_nodes, condition_factor):
    '''
    Give an id list of random nodes that fit a given condition.
    '''
    conditioned_list = []
    ids = [i for i in range(no_of_nodes)]

    for _ in range(int(no_of_nodes * condition_factor)):
        conditioned_list.append(ids.pop(np.random.randint(len(ids))))

    return conditioned_list


def calc_percentage(amount, total):
    '''
    Calculate the percentage of amount from the total.
    '''
    return 100 * amount / total


def wrap_func(func, *args, **kwargs):
    '''
    Create a wrapper around a function, so it can be timed.
    '''
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def time(func):
    '''
    Time a function.
    '''
    return timeit.timeit(func, number=1000) / 1000
