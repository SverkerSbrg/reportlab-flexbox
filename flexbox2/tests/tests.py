import unittest

from flexbox2.flex import FlexItem2, FlexBox2
from flexbox2.measurement import Measurement2Descriptor, FlexMeasurement2
from flexbox2.options import FlexStart2, FlexEnd2, FlexCenter2, SpaceAround2, SpaceEvenly2, SpaceBetween2, \
    FlexDirection2, FlexWrap2


class TestItem(FlexItem2):
    _content_width = Measurement2Descriptor()
    _content_height = Measurement2Descriptor()

    def __init__(self, content_width, content_height, **kwargs):
        self._content_width = content_width
        self._content_height = content_height

        super().__init__(**kwargs)

    def wrap_content(self, avail_width, avail_height):
        self._content_width.base = avail_width
        self._content_height.base = avail_height

        return float(self._content_width), float(self._content_height)




class WrapTestCase(unittest.TestCase):
    def test_auto_no_frame(self):
        item = TestItem(
            content_width=100,
            content_height=100
        )
        self.assertEqual((100, 100), item.wrap(0, 0))
        self.assertEqual((100, 100), item.wrap(1000, 1000))

    def test_auto_margin(self):
        item = TestItem(
            margin=10,
            content_width=100,
            content_height=100
        )
        self.assertEqual((120, 120), item.wrap(0, 0))

    def test_auto_padding(self):
        item = TestItem(
            padding=10,
            content_width=100,
            content_height=100
        )
        self.assertEqual((120, 120), item.wrap(0, 0))

    def test_auto_border(self):
        item = TestItem(
            border=10,
            content_width=100,
            content_height=100
        )
        self.assertEqual((120, 120), item.wrap(0, 0))

    def test_auto_all(self):
        item = TestItem(
            border=10,
            padding=20,
            margin=20,
            content_width=100,
            content_height=100
        )
        self.assertEqual((200, 200), item.wrap(0, 0))

    def test_full_width(self):
        item = TestItem(
            width="100%",
            height="100%",
            content_width=200,
            content_height=100,
            padding=25
        )
        self.assertEqual((50, 25), item.wrap(50, 25))

    def test_auto_fill(self):
        item = TestItem(
            content_width="100%",
            content_height=100,
            padding=10
        )
        self.assertEqual((20, 120), item.wrap(1000, 1000))


class OptionsTestCase(unittest.TestCase):
    def test_flex_start(self):
        self.assertEqual(
            tuple(FlexStart2.points((10, 10, 10), 100)),
            (0, 10, 20)
        )
        self.assertEqual(
            tuple(FlexStart2.points((10, 20, 30), 10)),
            (0, 10, 30)
        )
        self.assertEqual(
            tuple(FlexStart2.points((10,), 10)),
            (0,)
        )

    def test_flex_end(self):
        self.assertEqual(
            tuple(FlexEnd2.points((10, 10, 10), 100)),
            (70, 80, 90)
        )
        self.assertEqual(
            tuple(FlexEnd2.points((10, 20, 30), 10)),
            (-50, -40, -20)
        )
        self.assertEqual(
            tuple(FlexEnd2.points((10,), 20)),
            (10,)
        )

    def test_flex_center(self):
        self.assertEqual(
            tuple(FlexCenter2.points((10, 10, 10), 100)),
            (35, 45, 55)
        )
        self.assertEqual(
            tuple(FlexCenter2.points((10, 20, 30), 0)),
            (-30, -20, 0)
        )
        self.assertEqual(
            tuple(FlexCenter2.points((50,), 100)),
            (25, )
        )

    def test_space_around(self):
        self.assertEqual(
            tuple(SpaceAround2.points((50,), 100)),
            (25, )
        )

        self.assertEqual(
            tuple(SpaceAround2.points((10, 10), 100)),
            (20, 70)
        )

        self.assertEqual(
            tuple(SpaceAround2.points((100, 100), 150)),
            (-25, 75)
        )

    def test_space_evenly(self):
        self.assertEqual(
            tuple(SpaceEvenly2.points((50,), 100)),
            (25, )
        )

        self.assertEqual(
            tuple(SpaceEvenly2.points((20, 20), 100)),
            (20, 60)
        )

        self.assertEqual(
            tuple(SpaceEvenly2.points((10, 20, 30), 0)),
            (-30, -20, 0)
        )

    def test_space_between(self):
        self.assertEqual(
            tuple(SpaceBetween2.points((50,), 100)),
            (25, )
        )

        self.assertEqual(
            tuple(SpaceBetween2.points((10, 20, 30), 120)),
            (0, 40, 90)
        )

        self.assertEqual(
            tuple(SpaceBetween2.points((10, 20, 30), 0)),
            (-30, -20, 0)
        )


class TestBox3(FlexBox2):
    def wrap(self, avail_width, avail_height):
        print("\nwrap(%s, %s)" % (avail_width, avail_height))
        result = super().wrap(avail_width, avail_height)
        print("   ", result)
        return result

    def wrap_content(self, avail_width, avail_height):
        print("    wrap_content(%s, %s)" % (avail_width, avail_height))
        result = super().wrap_content(avail_width, avail_height)
        print("        ", result)
        return result


class FakeDrawItem(FlexItem2):
    def __init__(self, expected_x=None, expected_y=None, **kwargs):
        super().__init__(**kwargs)
        self.expected_x = expected_x
        self.expected_y = expected_y

    def drawOn(self, canvas, x, y, **kwargs):
        print("drawOnFake", x, y, self.expected_x, self.expected_y)
        # print(self.expected_x, x,  self.expected_y, self)
        if self.expected_x is not None:
            assert float(x) == float(self.expected_x)

        if self.expected_y is not None:
            assert float(y) == float(self.expected_y)


class FlexBoxWrapContentTest(unittest.TestCase):
    def test_row_no_wrap(self):
        box = FlexBox2(
            FlexItem2(width=100, height=100),
            FlexItem2(width=50, height=50),
        )

        self.assertEqual(
            box.wrap_content(1000, 1000),
            (150, 100)
        )
        self.assertEqual(
            box.wrap(1000, 1000),
            (150, 100)
        )

    def test_row_wrap(self):
        self.assertEqual(
            FlexBox2(
                FlexItem2(width=100, height=100),
                FlexItem2(width=50, height=50),
                flex_wrap=FlexWrap2.Wrap2
            ).wrap_content(0, 0),
            (100, 150)
        )

    def test_column_no_wrap(self):
        self.assertEqual(
            FlexBox2(
                FlexItem2(width=100, height=100),
                FlexItem2(width=50, height=50),
                flex_direction=FlexDirection2.Column2
            ).wrap_content(1000, 1000),
            (100, 150)
        )

    def test_column_wrap(self):
        self.assertEqual(
            FlexBox2(
                FlexItem2(width=100, height=100),
                FlexItem2(width=50, height=50),
                flex_direction=FlexDirection2.Column2,
                flex_wrap=FlexWrap2.Wrap2
            ).wrap_content(0, 0),
            (150, 100)
        )

# class FlexBoxDrawContentTestCase(unittest.TestCase):
#     def test_row_no_wrap(self):
#         box = FlexBox2(
#             FakeDrawItem(width=100, height=100, expected_x=0, expected_y=0),
#             FakeDrawItem(width=50, height=50, expected_x=100, expected_y=0),
#         )
#         box.wrap(0, 0)
#         box.canv = None
#         box.draw_content(box.width, box.height, box.content_width, box.content_height)


