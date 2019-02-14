""" Useful generic functions
"""
import collections


def update(d, u):
    """ Update nested dictionaries
    """
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
