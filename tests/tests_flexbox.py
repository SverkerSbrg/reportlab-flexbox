from itertools import zip_longest
from unittest import TestCase

from flexbox.options import FlexStart
from flexbox2.flex import FlexBox2, FlexItem2
from flexbox2.options import FlexDirection2, FlexWrap2, JustifyContent2, AlignContent2, AlignItems2, Stretch2, \
    SpaceBetween2


class TestBox(FlexBox2):
    canv = None

    def __init__(self, *items, avail_width=1000, avail_height=1000, **kwargs):
        self.avail_width = avail_width
        self.avail_height = avail_height

        super().__init__(*items, **kwargs)

    def wrap_content(self, avail_width, avail_height):
        self.avail_content_width = avail_width
        self.avail_content_height = avail_height

        return super().wrap_content(avail_width, avail_height)


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

    def assertRows(self, test_box, items_per_row):
        test_box.wrap(test_box.avail_width, test_box.avail_height)

        self.assertEqual(len(test_box.rows), len(items_per_row))
        for expected_item_count, row in zip(items_per_row, test_box.rows):
            self.assertEqual(expected_item_count, len(row))

    def assertWrapContent(self, test_box, expected_width, expected_height):
        width, height = test_box.wrap(test_box.avail_width, test_box.avail_height)
        self.assertEqual(expected_width, width)
        self.assertEqual(expected_height, height)

    def assertDrawItems(self, test_box, positions, top_left=True):
        width, height = test_box.wrap(test_box.avail_width, test_box.avail_height)
        test_box.draw_content(test_box.width, test_box.height, test_box.content_width, test_box.content_height)

        i = 0
        for item, expected_position in zip_longest(test_box.items, positions):

            position = (item.test_x, height - item.test_y - float(item.height) if top_left else item.test_y)
            self.assertEqual(
                position,
                expected_position,
                msg="Item %d was positioned on %s instead of %s." % (i, position, expected_position)
            )
            i += 1

    def assertContentSize(self, test_box, expected_width, expected_height):
        width, height = test_box.wrap(test_box.avail_width, test_box.avail_height)
        self.assertEqual(expected_width, test_box.avail_content_width)
        self.assertEqual(expected_height, test_box.avail_content_height)


    def test_single_item_auto_size(self):
        box = TestBox(
            TestItem(width=100, height=50)
        )
        self.assertWrap(box, 100, 50)
        self.assertDrawItems(box, [(0, 0),])

    def test_multiple_item_auto_size(self):
        box = TestBox(
            TestItem(width=100, height=70),
            TestItem(width=150, height=50)
        )
        self.assertWrap(box, 250, 70)
        self.assertDrawItems(box, [(0, 0), (100, 0)])

    def test_fixed_width_overflow(self):
        box = TestBox(
            TestItem(width=100, height=70),
            TestItem(width=150, height=50),
            width=100,
            height=100
        )
        self.assertWrap(box, 100, 100)
        self.assertDrawItems(box, [(0, 0), (100, 0)])


class FlexDirectionTestCase(FlexBoxTestCase):
    def test_row_no_wrap_single_item(self):
        box = TestBox(
            TestItem(width=100, height=50),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2
        )
        self.assertWrap(box, 100, 50)
        # self.assertDrawItems(box, [(0, 0)])

    def test_row_no_wap_multiple_items(self):
        box = TestBox(
            TestItem(width=100, height=50),
            TestItem(width=50, height=25),
            TestItem(width=10, height=5),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2
        )
        self.assertWrap(box, 160, 50)

    def test_column_no_wrap_single_item(self):
        box = TestBox(
            TestItem(width=100, height=50),
            flex_direction=FlexDirection2.Column2,
            flex_wrap=FlexWrap2.NoWrap2
        )
        self.assertWrap(box, 100, 50)
        # self.assertDrawItems(box, [(0, 0)])

    def test_column_no_wap_multiple_items(self):
        box = TestBox(
            TestItem(width=100, height=50),
            TestItem(width=50, height=25),
            TestItem(width=10, height=5),
            flex_direction=FlexDirection2.Column2,
            flex_wrap=FlexWrap2.NoWrap2
        )
        self.assertWrap(box, 100, 80)

    def test_row_wrap(self):
        box = TestBox(
            TestItem(width=40, height=50),
            TestItem(width=40, height=25),
            TestItem(width=40, height=5),
            TestItem(width=120, height=50),
            TestItem(width=60, height=50),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.Wrap2,
            width=120
        )
        self.assertWrap(box, 120, 150)
        self.assertRows(box, [3, 1, 1])

    def test_row_wrap_to_large_item(self):
        box = TestBox(
            TestItem(width=200, height=50),
            TestItem(width=50, height=50),
            TestItem(width=60, height=50),
            TestItem(width=40, height=50),
            TestItem(width=20, height=50),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.Wrap2,
            width=100
        )
        self.assertWrap(box, 100, 200)
        self.assertRows(box, [1, 1, 2, 1])

    def test_row_wrap_auto_width(self):
        box = TestBox(
            TestItem(width=40, height=20),
            TestItem(width=40, height=20),
            TestItem(width=40, height=20),
            TestItem(width=40, height=20),
            TestItem(width=40, height=20),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.Wrap2
        )
        self.assertWrap(box, 40, 100)
        self.assertRows(box, [1, 1, 1, 1, 1])

    def test_column_wrap(self):
        box = TestBox(
            TestItem(width=50, height=40),
            TestItem(width=25, height=40),
            TestItem(width=5, height=40),
            TestItem(width=50, height=120),
            TestItem(width=50, height=60),
            flex_direction=FlexDirection2.Column2,
            flex_wrap=FlexWrap2.Wrap2,
            height=120
        )
        self.assertWrap(box, 150, 120)
        self.assertRows(box, [3, 1, 1])

    def test_column_wrap_to_large_item(self):
        box = TestBox(
            TestItem(width=50, height=200),
            TestItem(width=50, height=50),
            TestItem(width=50, height=60),
            TestItem(width=50, height=40),
            TestItem(width=50, height=20),
            flex_direction=FlexDirection2.Column2,
            flex_wrap=FlexWrap2.Wrap2,
            height=100
        )
        self.assertWrap(box, 200, 100)
        self.assertRows(box, [1, 1, 2, 1])

    def test_column_wrap_auto_width(self):
        box = TestBox(
            TestItem(width=40, height=20),
            TestItem(width=40, height=20),
            TestItem(width=40, height=20),
            TestItem(width=40, height=20),
            TestItem(width=40, height=20),
            flex_direction=FlexDirection2.Column2,
            flex_wrap=FlexWrap2.Wrap2
        )
        self.assertWrap(box, 200, 20)
        self.assertRows(box, [1, 1, 1, 1, 1])

    def test_justify_content_flex_start_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexStart,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(0, 0)])

    def test_justify_content_flex_start_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexStart,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(0, 0), (20, 0), (40, 0)])

    def test_justify_content_flex_start_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexStart,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(0, 0), (20, 0), (40, 0)])

    def test_justify_content_flex_end_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexEnd,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(80, 0)])

    def test_justify_content_flex_end_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexEnd,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0), (60, 0), (80, 0)])

    def test_justify_content_flex_end_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexEnd,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-10, 0), (10, 0), (30, 0)])

    def test_justify_content_flex_center_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexCenter,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0)])

    def test_justify_content_flex_center_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexCenter,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(20, 0), (40, 0), (60, 0)])

    def test_justify_content_flex_center_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.FlexCenter,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-5, 0), (15, 0), (35, 0)])

    def test_justify_content_space_between_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceBetween,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0)])

    def test_justify_content_space_between_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceBetween,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(0, 0), (40, 0), (80, 0)])

    def test_justify_content_space_between_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceBetween,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-5, 0), (15, 0), (35, 0)])

    def test_justify_content_space_around_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceAround,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0)])

    def test_justify_content_space_around_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceAround,
            width=120
        )
        self.assertWrap(box, 120, 10)
        self.assertDrawItems(box, [(10, 0), (50, 0), (90, 0)])

    def test_justify_content_space_around_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceAround,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-5, 0), (15, 0), (35, 0)])

    def test_justify_content_space_evenly_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceEvenly,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0)])

    def test_justify_content_space_evenly_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceEvenly,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(10, 0), (40, 0), (70, 0)])

    def test_justify_content_space_evenly_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.NoWrap2,
            justify_content=JustifyContent2.SpaceEvenly,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-5, 0), (15, 0), (35, 0)])

    def test_align_content_flex_start(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap2.Wrap2,
            flex_direction=FlexDirection2.Row2,
            align_content=AlignContent2.FlexStart
        )
        self.assertDrawItems(box, [(0, 0), (0, 20), (0, 40)])

    def test_align_content_flex_end(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap2.Wrap2,
            flex_direction=FlexDirection2.Row2,
            align_content=AlignContent2.FlexEnd
        )
        self.assertDrawItems(box, [(0, 60), (0, 80), (0, 100)])

    def test_align_content_flex_center(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap2.Wrap2,
            flex_direction=FlexDirection2.Row2,
            align_content=AlignContent2.FlexCenter
        )
        self.assertDrawItems(box, [(0, 30), (0, 50), (0, 70)])

    def test_align_content_space_between(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap2.Wrap2,
            flex_direction=FlexDirection2.Row2,
            align_content=AlignContent2.SpaceBetween2
        )
        self.assertDrawItems(box, [(0, 0), (0, 50), (0, 100)])

    def test_align_content_space_around(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap2.Wrap2,
            flex_direction=FlexDirection2.Row2,
            align_content=AlignContent2.SpaceAround
        )
        self.assertDrawItems(box, [(0, 10), (0, 50), (0, 90)])

    def test_align_content_space_evenly(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap2.Wrap2,
            flex_direction=FlexDirection2.Row2,
            align_content=AlignContent2.SpaceEvenly
        )
        self.assertDrawItems(box, [(0, 15), (0, 50), (0, 85)])

    def test_align_content_stretch(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap2.Wrap2,
            flex_direction=FlexDirection2.Row2,
            align_content=AlignContent2.Stretch,
            align_items=AlignItems2.FlexStart
        )
        self.assertDrawItems(box, [(0, 0), (0, 40), (0, 80)])

    def test_align_items_flex_start(self):
        box = TestBox(
            TestItem(width=10, height=40),
            TestItem(width=10, height=20),
            TestItem(width=10, height=10),
            TestItem(width=10, height=10, align_self=AlignItems2.FlexEnd),
            align_items=AlignItems2.FlexStart
        )
        self.assertDrawItems(box, [(0, 0), (10, 0), (20, 0), (30, 30)])

    def test_align_items_flex_end(self):
        box = TestBox(
            TestItem(width=10, height=40),
            TestItem(width=10, height=20),
            TestItem(width=10, height=10),
            TestItem(width=10, height=10, align_self=AlignItems2.FlexStart),
            align_items=AlignItems2.FlexEnd
        )
        self.assertDrawItems(box, [(0, 0), (10, 20), (20, 30), (30, 0)])

    def test_align_items_flex_center(self):
        box = TestBox(
            TestItem(width=10, height=40),
            TestItem(width=10, height=20),
            TestItem(width=10, height=10),
            TestItem(width=10, height=10, align_self=AlignItems2.FlexStart),
            align_items=AlignItems2.FlexCenter
        )
        self.assertDrawItems(box, [(0, 0), (10, 10), (20, 15), (30, 0)])

    def test_align_self(self):
        box = TestBox(
            TestItem(width=20, height=10, align_self=AlignItems2.FlexStart),
            TestItem(width=20, height=10, align_self=AlignItems2.FlexCenter),
            TestItem(width=20, height=10, align_self=AlignItems2.FlexEnd),
            TestItem(width=20, height=10, align_self=AlignItems2.FlexStart),
            TestItem(width=20, height=10, align_self=AlignItems2.FlexCenter),
            TestItem(width=20, height=10, align_self=AlignItems2.FlexEnd),
            height=60,
            width=60,
            flex_wrap=FlexWrap2.Wrap2
        )
        self.assertDrawItems(box, [(0, 0), (20, 10), (40, 20), (0, 30), (20, 40), (40, 50)])

    def test_default_settings(self):
        box = TestBox()
        self.assertEqual(box.flex_direction, FlexDirection2.Row2)
        self.assertEqual(box.flex_wrap, FlexWrap2.NoWrap2)
        self.assertEqual(box.justify_content, JustifyContent2.FlexStart)
        self.assertEqual(box.align_items, AlignItems2.FlexStart)
        self.assertEqual(box.align_content, AlignContent2.Stretch)
        self.assertEqual(box.align_self, None)

    def test_size_relative_full(self):
        box = TestBox(
            width="100%",
            height="100%",
            avail_width=400,
            avail_height=200
        )
        self.assertWrap(box, 400, 200)

    def test_size_relative_half(self):
        box = TestBox(
            width="50%",
            height="50%",
            avail_width=400,
            avail_height=200
        )
        self.assertWrap(box, 200, 100)

    def test_size_fixed(self):
        box = TestBox(
            width=50,
            height=50,
            avail_width=400,
            avail_height=200
        )
        self.assertWrap(box, 50, 50)

    def test_margin_absolute_symmetric(self):
        box = TestBox(
            width=50,
            height=25,
            margin=5
        )
        self.assertContentSize(box, 40, 15)

    def test_margin_relative_symmetric(self):
        box = TestBox(
            width=50,
            height=25,
            margin="10%"
        )
        self.assertContentSize(box, 40, 20)

    def test_margin_asymmetric(self):
        box = TestBox(
            width=50,
            height=25,
            margin=("10%", 5, "10%"),
        )
        self.assertContentSize(box, 40, 20)
        
    def test_padding_absolute_symmetric(self):
        box = TestBox(
            width=50,
            height=25,
            padding=5
        )
        self.assertContentSize(box, 40, 15)

    def test_padding_relative_symmetric(self):
        box = TestBox(
            width=50,
            height=25,
            padding="10%"
        )
        self.assertContentSize(box, 40, 20)

    def test_padding_asymmetric(self):
        box = TestBox(
            width=50,
            height=25,
            padding=("10%", 5, "10%"),
        )
        self.assertContentSize(box, 40, 20)
        
    def test_border_absolute_symmetric(self):
        box = TestBox(
            width=50,
            height=25,
            border=5
        )
        self.assertContentSize(box, 40, 15)

    def test_border_relative_symmetric(self):
        box = TestBox(
            width=50,
            height=25,
            border="10%"
        )
        self.assertContentSize(box, 40, 20)

    def test_border_asymmetric(self):
        box = TestBox(
            width=50,
            height=25,
            border=("10%", 5, "10%"),
        )
        self.assertContentSize(box, 40, 20)

    def test_invalid_arguments(self):
        for attr, value in (
                ("flex_direction", FlexWrap2.NoWrap2),
                ("justify_content", Stretch2),
                ("align_items", SpaceBetween2),
                ("align_content", FlexDirection2.Row2),
                ("flex_wrap", FlexStart),
                ("flex_direction", False),
                ("justify_content", True),
                ("align_items", 2),
                ("align_content", []),
        ):
            with self.assertRaises(ValueError):
                box = TestBox()
                setattr(box, attr, value)





