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

    def __eq__(self, other):
        if isinstance(other, FlexMeasurement2):
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
            args.append(self.static)
        if self._relative:
            args.append("%s%%" % self.relative)

        if not args:
            return "0"

        return "+".join(args)

    def __repr__(self):
        return str(self)

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


class FlexFrame:
    top = Measurement2Descriptor()
    right = Measurement2Descriptor()
    bottom = Measurement2Descriptor()
    left = Measurement2Descriptor()

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

    @property
    def width_base(self):
        if self._width_base is None:
            raise Exception("Base not set.")
        return self._width_base

    @width_base.setter
    def width_base(self, value):
        self._width_base = value

        for measurement in (self.right, self.left):
            measurement.base = value
            
    @property
    def height_base(self):
        if self._height_base is None:
            raise Exception("Base not set.")
        return self._height_base

    @height_base.setter
    def height_base(self, value):
        self._height_base = value

        for measurement in (self.top, self.bottom):
            measurement.base = value

    @property
    def width(self):
        return self.left + self.right

    @property
    def height(self):
        return self.top + self.bottom


class FlexFrameDescriptor:
    def __init__(self):
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance not in self.values:
            self.values[instance] = FlexFrame()

        return self.values[instance]

    def __set__(self, instance, value):
        if type(value) in (str, int, float, FlexMeasurement2) or value is None:
            frame = FlexFrame(value)
        else:
            frame = FlexFrame(*value)

        self.values[instance] = frame