from itertools import chain
from weakref import WeakKeyDictionary


class CompoundFlexMeasurement:
    def __init__(self, positive=None, negative=None):
        self.positive = list(m for m in positive or [])
        self.negative = list(m for m in negative or [])

    def __float__(self):
        return sum(float(m) for m in self.positive) - sum(float(m) for m in self.negative)

    @property
    def static(self):
        return sum(m.static for m in self.positive) - sum(m.static for m in self.negative)

    @property
    def relative(self):
        return sum(m.relative for m in self.positive) - sum(m.relative for m in self.negative)

    @property
    def base(self):
        raise NotImplementedError()

    @base.setter
    def base(self, value):
        for m in chain(self.positive, self.negative):
            m.base = value

    def __add__(self, other):
        if isinstance(other, CompoundFlexMeasurement):
            return CompoundFlexMeasurement(chain(self.positive, other.positive), chain(self.negative, other.negative))
        if not isinstance(other, FlexMeasurement):
            other = FlexMeasurement.parse(other)
        return CompoundFlexMeasurement(chain(self.positive, [other]), self.negative)

    def __sub__(self, other):
        if isinstance(other, CompoundFlexMeasurement):
            return CompoundFlexMeasurement(chain(self.positive, other.negative), chain(self.negative, other.positive))
        if isinstance(other, FlexMeasurement):
            return CompoundFlexMeasurement(chain(self.positive), chain(self.negative, [other]))

    def __bool__(self):
        return any(chain(self.positive, self.negative))


class FlexMeasurement:
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
        if isinstance(other, CompoundFlexMeasurement):
            return CompoundFlexMeasurement(chain([self], other.positive), other.negative)
        if not isinstance(other, FlexMeasurement):
            other = FlexMeasurement.parse(other)
        return CompoundFlexMeasurement([self, other], [])

    def __sub__(self, other):
        if isinstance(other, CompoundFlexMeasurement):
            return CompoundFlexMeasurement(other.negative, chain(other.positive, [self]))
        if isinstance(other, FlexMeasurement):
            return CompoundFlexMeasurement([self], [other])

    def __bool__(self):
        return not (self._static is None and self._relative is None)

    def __eq__(self, other):
        if isinstance(other, FlexMeasurement):
            return (
                       self._static == other._static
                   ) and (
                       self._relative == other._relative
                   ) and (
                       self._base == other._base
                   )
        elif isinstance(other, float):
            return float(self) == other
        return False

    def __str__(self):
        args = []

        if self._static:
            args.append(str(self.static))
        if self._relative:
            args.append("%s%%" % self.relative)

        if not args:
            return "0"

        return "+".join(args)

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse(value):
        if issubclass(type(value), (FlexMeasurement, CompoundFlexMeasurement)):
            return value

        if value is None:
            return FlexMeasurement(None, None)

        if isinstance(value, (int, float)):
            return FlexMeasurement(value, 0)

        if isinstance(value, str):
            if "%" in value:
                return FlexMeasurement(0, float(value.replace("%", "")) / 100)
            else:
                return FlexMeasurement(float(value), 0)

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


class FlexMeasurementDescriptor:
    def __init__(self):
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        try:
            return self.values[instance]
        except KeyError:
            return None

    def __set__(self, instance, value):
        self.values[instance] = FlexMeasurement.parse(value)


class FlexFrame:
    top = FlexMeasurementDescriptor()
    right = FlexMeasurementDescriptor()
    bottom = FlexMeasurementDescriptor()
    left = FlexMeasurementDescriptor()

    _width_base = None
    _height_base = None

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

        self.width = self.right + self.left
        self.height = self.top + self.bottom

        # @property
        # def width_base(self):
        #     if self._width_base is None:
        #         raise Exception("Base not set.")
        #     return self._width_base
        #
        # @width_base.setter
        # def width_base(self, value):
        #     self._width_base = value
        #
        #     for measurement in (self.right, self.left):
        #         measurement.base = value
        #
        # @property
        # def height_base(self):
        #     if self._height_base is None:
        #         raise Exception("Base not set.")
        #     return self._height_base
        #
        # @height_base.setter
        # def height_base(self, value):
        #     self._height_base = value
        #
        #     for measurement in (self.top, self.bottom):
        #         measurement.base = value
        #
        # @property
        # def width(self):
        #     return self.left + self.right
        #
        # @property
        # def height(self):
        #     return self.top + self.bottom


class FlexFrameDescriptor:
    def __init__(self):
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance not in self.values:
            self.values[instance] = FlexFrame()

        return self.values[instance]

    def __set__(self, instance, value):
        if not isinstance(value, FlexFrame):
            if type(value) in (str, int, float, FlexMeasurement, CompoundFlexMeasurement) or value is None:
                value = FlexFrame(value)
            else:
                value = FlexFrame(*value)

        self.values[instance] = value
