import numpy as np
def subset_query(x, match_func):
    keep_idxs = [idx for idx, item in enumerate(x) if match_func(item)]
    return subset_idxs(x, keep_idxs)


def subset_idxs(x, keep_idxs):
    if keep_idxs is None:
        return x.copy()
    else:
        if len(keep_idxs) == 1:
            keep_idxs = [keep_idxs]
        return x[keep_idxs]
def sort(x, key):
    '''sort x by values of key - must be numbers'''
    return x[np.argsort(claim['amount'])[::-1]]


def sort_by(x, key, func, return_scores=True):
    '''sort the input array x by the key according to the score per key'''
    keys = np.unique(x[key])
    scores = np.zeros(len(keys))
    for idx, item in enumerate(x):
        scores[np.where(keys == item[key])] += func(item)

    sorted_ids = np.argsort(scores)[::-1]
    if return_scores:
        return keys[sorted_ids], scores[sorted_ids]
    else:
        return keys[sorted_ids]

def split_by(x, key):
    '''split an array into multiple arrays with matching values of key'''
    keys = np.unique(x[key])
    split_dict = {}
    for k in keys:
        split_dict[k] = []
    for item in x:
        split_dict[item[key]].append(item)
    for key in split_dict.keys():
        split_dict[key] = np.asarray(split_dict[key], dtype=x.dtype)
    return split_dict


def average(x, key, value_key, return_split=False):
    '''average x[value_key] per unique element in x[key]'''
    split = split_by(x, key)
    split_averages = {}
    for k in split.keys():
        split_averages[k] = split[k][value_key].mean()
    if return_split:
        return split_averages, split
    else:
        return split_averages
