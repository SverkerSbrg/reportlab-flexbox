from weakref import WeakKeyDictionary

from reportlab.lib.colors import HexColor


class ColorDescriptor():
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __set__(self, instance, value):
        if isinstance(value, HexColor):
            pass
        elif isinstance(value, int):
            value = HexColor(value)
        elif isinstance(value, tuple) and len(value) == 3:



        self._values[instance] = value