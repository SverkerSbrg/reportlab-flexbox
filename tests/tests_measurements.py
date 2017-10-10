import unittest

from flexbox import FlexMeasurement, FlexFrame


class ParseFlexMeasurementTestCase(unittest.TestCase):
    def assertMeasurement(self, expression, static, relative, base=None):
        measurement = FlexMeasurement.parse(expression)
        if base is not None:
            measurement.base = base
        self.assertEqual(measurement, FlexMeasurement(static, relative))

    def test_parse_int(self):
        for value in (
            -10,
            20,
            0
        ):
            self.assertMeasurement(value, value, 0)

    def test_parse_float(self):
        for value in (
            -10.0,
            20.32,
            0.000001
        ):
            self.assertMeasurement(value, value, 0)

    def test_parse_string(self):
        for value, static, relative in (
                ("100%", 0, 1),
                ("20%", 0, 0.2),
                ("-10%", 0, -0.1),
                ("10", 10, 0)
        ):
            self.assertMeasurement(value, static, relative)

    def test_parse_measurement(self):
        for value, static, relative in (
                (FlexMeasurement(10, 0), 10, 0),
                (FlexMeasurement(10, 0.1), 10, 0.1),
                (FlexMeasurement(0, 0.5), 0, 0.5),
                (FlexMeasurement(0, 0), 0, 0),
        ):
            self.assertMeasurement(value, static, relative)


class FrameTestCase(unittest.TestCase):
    def assertFrame(self, frame, top, right, bottom, left):
        self.assertEqual(frame.top, FlexMeasurement(static=top[0], relative=top[1]))
        self.assertEqual(frame.right, FlexMeasurement(static=right[0], relative=right[1]))
        self.assertEqual(frame.bottom, FlexMeasurement(static=bottom[0], relative=bottom[1]))
        self.assertEqual(frame.left, FlexMeasurement(static=left[0], relative=left[1]))

    def test_symmetric_absolute(self):
        self.assertFrame(FlexFrame(10), (10, 0), (10, 0), (10, 0), (10, 0))

    def test_symmetric_relative(self):
        self.assertFrame(FlexFrame("10%"), (0, 0.1), (0, 0.1), (0, 0.1), (0, 0.1))

    def test_2_pos_args(self):
        self.assertFrame(FlexFrame(5, "10%"), (5, 0), (0, 0.1), (5, 0), (0, 0.1))

    def test_3_pos_args(self):
        self.assertFrame(FlexFrame(5, "10%", 10), (5, 0), (0, 0.1), (10, 0), (0, 0.1))

    def test_4_pos_args(self):
        self.assertFrame(FlexFrame(5, "10%", 10, 15), (5, 0), (0, 0.1), (10, 0), (15, 0))


