from weakref import WeakKeyDictionary

from reportlab.lib.colors import HexColor, toColor


class ColorDescriptor:
    def __init__(self, default=None):
        self.values = WeakKeyDictionary()
        self.default = default

    def __set__(self, instance, value):
        if value is None:
            if instance in self.values:
                del self.values[instance]
        else:
            self.values[instance] = toColor(value)

    def __get__(self, instance, owner):
        try:
            return self.values[instance]
        except KeyError:
            return self.default
