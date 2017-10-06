from weakref import WeakKeyDictionary


class FlexMeasurement2:
    def __init__(self, static=None, relative=None):
        self._static = static
        self._relative = relative
        self._base = None

    @property
    def base(self):
        if self._base is None:
            raise Exception("Base not set.")
        return self._base

    @base.setter
    def base(self, value):
        self._base = value

    @property
    def static(self):
        return self._static or 0

    @property
    def relative(self):
        return self._relative or 0

    def __float__(self):
        return float(self.static + self.relative * self.base)

    def __add__(self, other):
        return self.__float__() + float(other)

    def __sub__(self, other):
        return self.__float__() - float(other)

    def __bool__(self):
        return not (self._static is None and self._relative is None)

    @staticmethod
    def parse(value):
        if issubclass(type(value), FlexMeasurement2):
            return value

        if value is None:
            return FlexMeasurement2(None, None)

        if isinstance(value, (int, float)):
            return FlexMeasurement2(value, 0)

        if isinstance(value, str) and "%" in value:
            return FlexMeasurement2(0, float(value.replace("%", "")) / 100)

        raise Exception("Unable to parse measurement '%s'" % value)

    @staticmethod
    def max(*measurements):
        measurements = tuple(float(m) for m in measurements if m)
        if measurements:
            return max(measurements)
        else:
            return None

    @staticmethod
    def min(*measurements):
        measurements = tuple(float(m) for m in measurements if m)
        if measurements:
            return min(measurements)
        else:
            return None


class Measurement2Descriptor:
    def __init__(self):
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        try:
            return self.values[instance]
        except KeyError:
            return None

    def __set__(self, instance, value):
        self.values[instance] = FlexMeasurement2.parse(value)


class Frame2:
    top = Measurement2Descriptor()
    right = Measurement2Descriptor()
    bottom = Measurement2Descriptor()
    left = Measurement2Descriptor()

    _base = None

    def __init__(self, *measurements):
        if len(measurements) == 1:
            self.top = measurements[0]
            self.right = measurements[0]
            self.bottom = measurements[0]
            self.left = measurements[0]
        elif len(measurements) == 2:
            self.top = measurements[0]
            self.right = measurements[1]
            self.bottom = measurements[0]
            self.left = measurements[1]
        elif len(measurements) == 3:
            self.top = measurements[0]
            self.right = measurements[1]
            self.bottom = measurements[2]
            self.left = measurements[1]
        elif len(measurements) == 4:
            self.top = measurements[0]
            self.right = measurements[1]
            self.bottom = measurements[2]
            self.left = measurements[3]
        else:
            self.top = None
            self.right = None
            self.bottom = None
            self.left = None

    @property
    def base(self):
        if self._base is None:
            raise Exception("Base not set.")
        return self._base

    @base.setter
    def base(self, value):
        self._base = value

        for measurement in (self.top, self.right, self.bottom, self.left):
            measurement.base = value

    @property
    def width(self):
        return self.left + self.right

    @property
    def height(self):
        return self.top + self.bottom


class FrameDescriptor:
    def __init__(self):
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance not in self.values:
            self.values[instance] = Frame2()

        return self.values[instance]

    def __set__(self, instance, value):
        self.values[instance] = Frame2(value)