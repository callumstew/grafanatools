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
        super().__init__(*args, **kwargs)
        update(self, dict_kwargs)
        self.__dict__ = self

    def _properties(self):
        props = set([p for p in self.__dir__() if p[0] != '_'])
        return props.difference(set(dict().__dir__()))


class Option(Item):
    selected = False
    text = ''
    value = ''


class Variable(Item):
    current = {}
    options = []

    def __init__(self, value, *args, **kwargs):
        self.current['text'] = str(value)
        self.current['value'] = value
        self.options.append(Option(text=str(value), value=value,
                                   selected=True))
        super().__init__(*args, **kwargs)


class Constant(Variable):
    type = 'constant'


class Textbox(Variable):
    type = 'textbox'


class Custom(Variable):
    type = 'custom'


class Interval(Variable):
    type = 'interval'


class DataSource(Item):
    type = 'datasource'
    current = {}

    def __init__(self, name, value, query, *args, **kwargs):
        self.current['text'] = str(value)
        self.current['value'] = value
        self.name = name
        self.query = query
        super().__init__(*args, **kwargs)
