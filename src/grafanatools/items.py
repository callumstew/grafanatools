""" Classes with JSON representation for where creating an object
is prefereable to writing it out fully
"""
from .generic import update


class Item(dict):

    def __init__(self, *args, **kwargs):
        for p in self._properties():
            self[p] = self.__getattribute__(p)
        dict_kwargs = {}
        for k, v in kwargs.items():
            if isinstance(v, dict):
                dict_kwargs[k] = kwargs.pop(k)
        super(Item, self).__init__(*args, **kwargs)
        update(self, dict_kwargs)
        self.__dict__ = self

    def _properties(self):
        props = set([p for p in self.__dir__() if p[0] != '_'])
        return props.difference(set(dict().__dir__()))


class Constant(Item):
    a = 1
