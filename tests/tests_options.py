import unittest

from flexbox.options import FlexStart, FlexEnd, FlexCenter, SpaceAround, SpaceEvenly, SpaceBetween


class OptionsTestCase(unittest.TestCase):
    def test_flex_start(self):
        self.assertEqual(
            tuple(FlexStart.points((10, 10, 10), 100)),
            (0, 10, 20)
        )
        self.assertEqual(
            tuple(FlexStart.points((10, 20, 30), 10)),
            (0, 10, 30)
        )
        self.assertEqual(
            tuple(FlexStart.points((10,), 10)),
            (0,)
        )

    def test_flex_end(self):
        self.assertEqual(
            tuple(FlexEnd.points((10, 10, 10), 100)),
            (70, 80, 90)
        )
        self.assertEqual(
            tuple(FlexEnd.points((10, 20, 30), 10)),
            (-50, -40, -20)
        )
        self.assertEqual(
            tuple(FlexEnd.points((10,), 20)),
            (10,)
        )

    def test_flex_center(self):
        self.assertEqual(
            tuple(FlexCenter.points((10, 10, 10), 100)),
            (35, 45, 55)
        )
        self.assertEqual(
            tuple(FlexCenter.points((10, 20, 30), 0)),
            (-30, -20, 0)
        )
        self.assertEqual(
            tuple(FlexCenter.points((50,), 100)),
            (25, )
        )

    def test_space_around(self):
        self.assertEqual(
            tuple(SpaceAround.points((50,), 100)),
            (25, )
        )

        self.assertEqual(
            tuple(SpaceAround.points((10, 10), 100)),
            (20, 70)
        )

        self.assertEqual(
            tuple(SpaceAround.points((100, 100), 150)),
            (-25, 75)
        )

    def test_space_evenly(self):
        self.assertEqual(
            tuple(SpaceEvenly.points((50,), 100)),
            (25, )
        )

        self.assertEqual(
            tuple(SpaceEvenly.points((20, 20), 100)),
            (20, 60)
        )

        self.assertEqual(
            tuple(SpaceEvenly.points((10, 20, 30), 0)),
            (-30, -20, 0)
        )

    def test_space_between(self):
        self.assertEqual(
            tuple(SpaceBetween.points((50,), 100)),
            (25, )
        )

        self.assertEqual(
            tuple(SpaceBetween.points((10, 20, 30), 120)),
            (0, 40, 90)
        )

        self.assertEqual(
            tuple(SpaceBetween.points((10, 20, 30), 0)),
            (-30, -20, 0)
        )
