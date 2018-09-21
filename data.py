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
