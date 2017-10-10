import unittest

from flexbox2.measurement import FlexFrame, FlexMeasurement


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


