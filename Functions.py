import numpy as np


def print_progress(current_epoch, total_epochs, progress_len=20):
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
            ["#" for _ in range(progress_bar_progress - 1)]
        )
        progress_bar += "".join(["." for _ in range(unprogressed)])
        progress_bar += "]"
        print(f"{progress_bar} {progress}%")


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
