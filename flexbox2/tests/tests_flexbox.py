from itertools import zip_longest
from unittest import TestCase

from flexbox2.flex import FlexBox2, FlexItem2


class TestBox(FlexBox2):
    canv = None

    def __init__(self, *items, avail_width=None, avail_height=None, **kwargs):
        self.avail_width = avail_width
        self.avail_height = avail_height

        super().__init__(*items, **kwargs)


class TestItem(FlexItem2):
    test_x = None
    test_y = None

    def __init__(self, *args, flag=None, **kwargs):
        if flag is not None:
            setattr(self, "flag", True)

        super().__init__(*args, **kwargs)

    def drawOn(self, canvas, x, y, _sW=0):
        self.test_x = x
        self.test_y = y


class FlexBoxTestCase(TestCase):
    def assertWrap(self, test_box, expected_width, expected_height):
        width, height = test_box.wrap(test_box.avail_width, test_box.avail_height)
        self.assertEqual(expected_width, width)
        self.assertEqual(expected_height, height)

    def assertWrapContent(self, test_box, expected_width, expected_height):
        width, height = test_box.wrap(test_box.avail_width, test_box.avail_height)
        self.assertEqual(expected_width, width)
        self.assertEqual(expected_height, height)

    def assertDrawItems(self, test_box, positions):
        test_box.wrap(test_box.avail_width, test_box.avail_height)
        test_box.draw_content(test_box.width, test_box.height, test_box.content_width, test_box.content_height)

        i = 0
        for item, expected_position in zip_longest(test_box.items, positions):

            position = (item.test_x, item.test_y)
            self.assertEqual(
                position,
                expected_position,
                msg="Item %d was positioned on %s instead of %s." % (i, position, expected_position)
            )
            i += 1

    def test_single_item_auto_size(self):
        box = TestBox(
            TestItem(width=100, height=50),
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 100, 50)
        self.assertDrawItems(box, [(0, 0),])

    def test_multiple_item_auto_size(self):
        box = TestBox(
            TestItem(width=100, height=70),
            TestItem(width=150, height=50),
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 250, 70)
        self.assertDrawItems(box, [(0, 0), (100, 20)])

    def test_fixed_width_overflow(self):
        box = TestBox(
            TestItem(width=100, height=70),
            TestItem(width=150, height=50),
            width=100,
            height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 100, 100)
        self.assertDrawItems(box, [(0, 30), (100, 50)])