from weakref import WeakKeyDictionary


class FlexMeasurement:
    def __init__(self, static=None, relative=None):
        self._static = static
        self._relative = relative

    @property
    def static(self):
        return self._static or 0

    @property
    def relative(self):
        return self._relative or 0

    def length(self, parent_length):
        return self.static + self.relative * parent_length

    def parent_length(self, content_length):
        return (self.static + content_length) / (1 - self.relative)

    @staticmethod
    def parse(value):
        if issubclass(type(value), FlexMeasurement):
            return value

        if value is None:
            return FlexMeasurement(None, None)

        if isinstance(value, (int, float)):
            return FlexMeasurement(value, 0)

        if isinstance(value, str) and "%" in value:
            return FlexMeasurement(0, float(value.replace("%", "")) / 100)

        raise Exception("Unable to parse measurement '%s'" % value)

    def __add__(self, other):
        if not isinstance(other, FlexMeasurement):
            other = FlexMeasurement.parse(other)

        if not (self and other):
            return FlexMeasurement(None, None)

        return FlexMeasurement(
            self.static + other.static if not (self._static is None and other._static is None) else None,
            self.relative + other.relative if not (self._relative is None and other._relative is None) else None
        )

    def __sub__(self, other):
        if not isinstance(other, FlexMeasurement):
            other = FlexMeasurement.parse(other)
        return FlexMeasurement(self.static - other.static, self.relative - other.relative)

    def __bool__(self):
        return not (self._static is None and self._relative is None)

    def __str__(self):
        return "%s %s%%" % (self.static, self.relative)


class MeasurementDescriptor:
    def __init__(self):
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        try:
            return self.values[instance]
        except KeyError:
            return None

    def __set__(self, instance, value):
        self.values[instance] = FlexMeasurement.parse(value)

    def length(self, parent_length):
        raise NotImplemented()


class BoundMeasurement:
    base = MeasurementDescriptor()
    min = MeasurementDescriptor()
    max = MeasurementDescriptor()

    def __init__(self, base, min, max):
        self.base = base
        self.min = min
        self.max = max

    def length(self, parent_length):
        return self.fit(self.base.length(parent_length), parent_length)

    def fit(self, absolut_length, parent_length):
        length = absolut_length
        if self.max:
            length = min(self.max.length(parent_length), length)
        if self.min:
            length = max(self.min.length(parent_length), length)
        return length

    def __bool__(self):
        return bool(self.base)

    def __str__(self):
        return str({"min": str(self.min), "base": str(self.base), "max": str(self.max)}) + str(self.base.length(0))


class Frame:
    top = MeasurementDescriptor()
    right = MeasurementDescriptor()
    bottom = MeasurementDescriptor()
    left = MeasurementDescriptor()

    def __init__(self, top, right, bottom, left, default=0):
        self.top = top or default
        self.right = right or default
        self.bottom = bottom or default
        self.left = left or default

    @property
    def width(self):
        return self.right + self.left

    @property
    def height(self):
        return self.top + self.bottom
