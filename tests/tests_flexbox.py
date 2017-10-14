from itertools import zip_longest
from unittest import TestCase

from flexbox import FlexBox, FlexItem, FlexMeasurement, FlexDirection, FlexWrap, JustifyContent, AlignContent, \
    AlignItems
from flexbox.options import Stretch, SpaceBetween, FlexStart


class TestBox(FlexBox):
    canv = None

    def __init__(self, *items, avail_width=1000, avail_height=1000, **kwargs):
        self.avail_width = avail_width
        self.avail_height = avail_height

        super().__init__(*items, **kwargs)

        self.kwargs.update({
            "avail_width": avail_width,
            "avail_height": avail_height
        })

    def wrap_content(self, avail_width, avail_height):
        self.avail_content_width = avail_width
        self.avail_content_height = avail_height

        return super().wrap_content(avail_width, avail_height)


class TestItem(FlexItem):
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
        test_box.draw_content(float(test_box.width), float(test_box.height), test_box.content_width, test_box.content_height)

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


class DebugBox(TestBox):
    def wrap(self, avail_width, avail_height):
        print("DebugBox.wrap(%s, %s)" % (avail_width, avail_height))

        for measurement in (self.min_width, self.width, self.max_width):
            measurement.base = avail_width
        for measurement in (self.min_height, self.height, self.max_height):
            measurement.base = avail_height

        width = FlexMeasurement.max(self.width, self.min_width)
        if width:
            width = FlexMeasurement.min(width, self.max_width)
        height = FlexMeasurement.max(self.height, self.min_height)
        if height:
            height = FlexMeasurement.min(height, self.max_height)

        print("   self", width, height)

        self.padding.width_base = width or 0
        self.margin.width_base = width or 0
        self.border.width_base = width or 0

        self.padding.height_base = height or 0
        self.margin.height_base = height or 0
        self.border.height_base = height or 0

        frame_width = self.padding.width + self.margin.width + self.border.width
        frame_height = self.padding.height + self.margin.height + self.border.height

        content_width, content_height = self.wrap_content(
            width - frame_width if width else avail_width,
            height - frame_height if height else avail_height
        )

        print("    content", content_width, content_height)

        if width is None or height is None:
            if width is None:
                width = FlexMeasurement.min(content_width + frame_width)
            if height is None:
                height = FlexMeasurement.min(content_height + frame_height)

            content_width, content_height = self.wrap_content(width - frame_width, height - frame_height)

        self.content_width = content_width
        self.content_height = content_height

        self.width = width
        self.width.base = 0
        self.height = height
        self.height.base = 0

        return width, height


class FlexDirectionTestCase(FlexBoxTestCase):
    def test_row_no_wrap_single_item(self):
        box = TestBox(
            TestItem(width=100, height=50),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap
        )
        self.assertWrap(box, 100, 50)
        # self.assertDrawItems(box, [(0, 0)])

    def test_row_no_wap_multiple_items(self):
        box = TestBox(
            TestItem(width=100, height=50),
            TestItem(width=50, height=25),
            TestItem(width=10, height=5),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap
        )
        self.assertWrap(box, 160, 50)

    def test_column_no_wrap_single_item(self):
        box = TestBox(
            TestItem(width=100, height=50),
            flex_direction=FlexDirection.Column,
            flex_wrap=FlexWrap.NoWrap
        )
        self.assertWrap(box, 100, 50)
        # self.assertDrawItems(box, [(0, 0)])

    def test_column_no_wap_multiple_items(self):
        box = TestBox(
            TestItem(width=100, height=50),
            TestItem(width=50, height=25),
            TestItem(width=10, height=5),
            flex_direction=FlexDirection.Column,
            flex_wrap=FlexWrap.NoWrap
        )
        self.assertWrap(box, 100, 80)

    def test_row_wrap(self):
        box = TestBox(
            TestItem(width=40, height=50),
            TestItem(width=40, height=25),
            TestItem(width=40, height=5),
            TestItem(width=120, height=50),
            TestItem(width=60, height=50),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.Wrap,
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
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.Wrap,
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
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.Wrap
        )
        self.assertWrap(box, 200, 20)
        self.assertRows(box, [5])

    def test_column_wrap(self):
        box = TestBox(
            TestItem(width=50, height=40),
            TestItem(width=25, height=40),
            TestItem(width=5, height=40),
            TestItem(width=50, height=120),
            TestItem(width=50, height=60),
            flex_direction=FlexDirection.Column,
            flex_wrap=FlexWrap.Wrap,
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
            flex_direction=FlexDirection.Column,
            flex_wrap=FlexWrap.Wrap,
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
            flex_direction=FlexDirection.Column,
            flex_wrap=FlexWrap.Wrap
        )
        self.assertWrap(box, 40, 100)
        self.assertRows(box, [5,])

    def test_justify_content_flex_start_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexStart,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(0, 0)])

    def test_justify_content_flex_start_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexStart,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(0, 0), (20, 0), (40, 0)])

    def test_justify_content_flex_start_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexStart,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(0, 0), (20, 0), (40, 0)])

    def test_justify_content_flex_end_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexEnd,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(80, 0)])

    def test_justify_content_flex_end_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexEnd,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0), (60, 0), (80, 0)])

    def test_justify_content_flex_end_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexEnd,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-10, 0), (10, 0), (30, 0)])

    def test_justify_content_flex_center_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexCenter,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0)])

    def test_justify_content_flex_center_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexCenter,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(20, 0), (40, 0), (60, 0)])

    def test_justify_content_flex_center_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.FlexCenter,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-5, 0), (15, 0), (35, 0)])

    def test_justify_content_space_between_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceBetween,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0)])

    def test_justify_content_space_between_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceBetween,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(0, 0), (40, 0), (80, 0)])

    def test_justify_content_space_between_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceBetween,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-5, 0), (15, 0), (35, 0)])

    def test_justify_content_space_around_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceAround,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0)])

    def test_justify_content_space_around_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceAround,
            width=120
        )
        self.assertWrap(box, 120, 10)
        self.assertDrawItems(box, [(10, 0), (50, 0), (90, 0)])

    def test_justify_content_space_around_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceAround,
            width=50
        )
        self.assertWrap(box, 50, 10)
        self.assertDrawItems(box, [(-5, 0), (15, 0), (35, 0)])

    def test_justify_content_space_evenly_single(self):
        box = TestBox(
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceEvenly,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(40, 0)])

    def test_justify_content_space_evenly_multiple(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceEvenly,
            width=100
        )
        self.assertWrap(box, 100, 10)
        self.assertDrawItems(box, [(10, 0), (40, 0), (70, 0)])

    def test_justify_content_space_evenly_overflow(self):
        box = TestBox(
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            TestItem(width=20, height=10),
            flex_direction=FlexDirection.Row,
            flex_wrap=FlexWrap.NoWrap,
            justify_content=JustifyContent.SpaceEvenly,
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
            flex_wrap=FlexWrap.Wrap,
            flex_direction=FlexDirection.Row,
            align_content=AlignContent.FlexStart
        )
        self.assertDrawItems(box, [(0, 0), (0, 20), (0, 40)])

    def test_align_content_flex_end(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap.Wrap,
            flex_direction=FlexDirection.Row,
            align_content=AlignContent.FlexEnd
        )
        self.assertDrawItems(box, [(0, 60), (0, 80), (0, 100)])

    def test_align_content_flex_center(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap.Wrap,
            flex_direction=FlexDirection.Row,
            align_content=AlignContent.FlexCenter
        )
        self.assertDrawItems(box, [(0, 30), (0, 50), (0, 70)])

    def test_align_content_space_between(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap.Wrap,
            flex_direction=FlexDirection.Row,
            align_content=AlignContent.SpaceBetween2
        )
        self.assertDrawItems(box, [(0, 0), (0, 50), (0, 100)])

    def test_align_content_space_around(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap.Wrap,
            flex_direction=FlexDirection.Row,
            align_content=AlignContent.SpaceAround
        )
        self.assertDrawItems(box, [(0, 10), (0, 50), (0, 90)])

    def test_align_content_space_evenly(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap.Wrap,
            flex_direction=FlexDirection.Row,
            align_content=AlignContent.SpaceEvenly
        )
        self.assertDrawItems(box, [(0, 15), (0, 50), (0, 85)])

    def test_align_content_stretch(self):
        box = TestBox(
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            TestItem(width=120, height=20),
            width=120,
            height=120,
            flex_wrap=FlexWrap.Wrap,
            flex_direction=FlexDirection.Row,
            align_content=AlignContent.Stretch,
            align_items=AlignItems.FlexStart
        )
        self.assertDrawItems(box, [(0, 0), (0, 40), (0, 80)])

    def test_align_items_flex_start(self):
        box = TestBox(
            TestItem(width=10, height=40),
            TestItem(width=10, height=20),
            TestItem(width=10, height=10),
            TestItem(width=10, height=10, align_self=AlignItems.FlexEnd),
            align_items=AlignItems.FlexStart
        )
        self.assertDrawItems(box, [(0, 0), (10, 0), (20, 0), (30, 30)])

    def test_align_items_flex_end(self):
        box = TestBox(
            TestItem(width=10, height=40),
            TestItem(width=10, height=20),
            TestItem(width=10, height=10),
            TestItem(width=10, height=10, align_self=AlignItems.FlexStart),
            align_items=AlignItems.FlexEnd
        )
        self.assertDrawItems(box, [(0, 0), (10, 20), (20, 30), (30, 0)])

    def test_align_items_flex_center(self):
        box = TestBox(
            TestItem(width=10, height=40),
            TestItem(width=10, height=20),
            TestItem(width=10, height=10),
            TestItem(width=10, height=10, align_self=AlignItems.FlexStart),
            align_items=AlignItems.FlexCenter
        )
        self.assertDrawItems(box, [(0, 0), (10, 10), (20, 15), (30, 0)])

    def test_align_self(self):
        box = TestBox(
            TestItem(width=20, height=10, align_self=AlignItems.FlexStart),
            TestItem(width=20, height=10, align_self=AlignItems.FlexCenter),
            TestItem(width=20, height=10, align_self=AlignItems.FlexEnd),
            TestItem(width=20, height=10, align_self=AlignItems.FlexStart),
            TestItem(width=20, height=10, align_self=AlignItems.FlexCenter),
            TestItem(width=20, height=10, align_self=AlignItems.FlexEnd),
            height=60,
            width=60,
            flex_wrap=FlexWrap.Wrap
        )
        self.assertDrawItems(box, [(0, 0), (20, 10), (40, 20), (0, 30), (20, 40), (40, 50)])

    def test_default_settings(self):
        box = TestBox()
        self.assertEqual(box.flex_direction, FlexDirection.Row)
        self.assertEqual(box.flex_wrap, FlexWrap.NoWrap)
        self.assertEqual(box.justify_content, JustifyContent.FlexStart)
        self.assertEqual(box.align_items, AlignItems.FlexStart)
        self.assertEqual(box.align_content, AlignContent.Stretch)
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
                ("flex_direction", FlexWrap.NoWrap),
                ("justify_content", Stretch),
                ("align_items", SpaceBetween),
                ("align_content", FlexDirection.Row),
                ("flex_wrap", FlexStart),
                ("flex_direction", False),
                ("justify_content", True),
                ("align_items", 2),
                ("align_content", []),
        ):
            with self.assertRaises(ValueError):
                box = TestBox()
                setattr(box, attr, value)

    def test_bug_auto_sizing_failing_when_child_uses_relative_measurements(self):
        # Fixed
        box = TestBox(
            TestItem(width="100%", height=20),
            avail_width=200,
            avail_height=200
        )
        self.assertWrap(box, 200, 20)

    def test_size_min_greedy_content(self):
        box = TestBox(
            TestItem(width="100%", height="100%"),
            min_width=200,
            min_height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 1000, 1000)

    def test_size_min_small_fixed_content(self):
        box = TestBox(
            TestItem(width=100, height=50),
            min_width=200,
            min_height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 200, 100)

    def test_size_min_large_fixed_content(self):
        box = TestBox(
            TestItem(width=400, height=200),
            min_width=200,
            min_height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 400, 200)

    def test_size_base_greedy_content(self):
        box = TestBox(
            TestItem(width="100%", height="100%"),
            width=200,
            height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 200, 100)

    def test_size_base_small_fix_content(self):
        box = TestBox(
            TestItem(width=100, height=50),
            width=200,
            height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 200, 100)

    def test_size_base_large_fix_content(self):
        box = TestBox(
            TestItem(width=400, height=200),
            width=200,
            height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 200, 100)

    def test_size_max_greedy_content(self):
        box = TestBox(
            TestItem(width="100%", height="100%"),
            max_width=200,
            max_height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 200, 100)

    def test_size_max_small_fix_content(self):
        box = TestBox(
            TestItem(width=100, height=50),
            max_width=200,
            max_height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 100, 50)

    def test_size_max_large_fix_content(self):
        box = TestBox(
            TestItem(width=400, height=200),
            max_width=200,
            max_height=100,
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 200, 100)

    def test_max_and_base_limit(self):
        box = TestBox(
            width=100,
            height=80,
            max_width="50%",
            max_height="50%",
            avail_width=150,
            avail_height=120
        )
        self.assertWrap(box, 75, 60)

    def test_max_and_base_no_limit(self):
        box = TestBox(
            width=100,
            height=80,
            max_width="50%",
            max_height="50%",
            avail_width=1000,
            avail_height=1000
        )
        self.assertWrap(box, 100, 80)

    def test_min_and_base_limit(self):
        box = TestBox(
            width=100,
            height=80,
            min_width="50%",
            min_height="50%",
            avail_width=1000,
            avail_height=500
        )
        self.assertWrap(box, 500, 250)

    def test_min_and_base_no_limit(self):
        box = TestBox(
            width=100,
            height=80,
            min_width="50%",
            min_height="50%",
            avail_width=0,
            avail_height=0
        )
        self.assertWrap(box, 100, 80)

    def test_split_rows(self):
        box = TestBox(
            TestItem(width="50%", height=10),
            TestItem(width="50%", height=10),
            TestItem(width="100%", height=10),
            TestItem(width="50%", height=10),
            width="100%",
            flex_wrap=FlexWrap.Wrap,
            avail_width=100,
            avail_height=100
        )
        self.assertWrap(box, 100, 30)
        box1, box2 = box.split(100, 15)
        self.assertWrap(box1, 100, 10)
        self.assertWrap(box2, 100, 20)

    def test_split_columns(self):
        box = TestBox(
            TestItem(width="50%", height=10),
            TestItem(width="50%", height=10),
            TestItem(width="100%", height=10),
            TestItem(width="50%", height=10),
            width="100%",
            flex_wrap=FlexWrap.NoWrap,
            flex_direction=FlexDirection.Column,
            avail_width=100,
            avail_height=100
        )
        self.assertWrap(box, 100, 40)
        box1, box2 = box.split(100, 15)
        self.assertWrap(box1, 100, 10)
        self.assertWrap(box2, 100, 30)

    def test_no_split_no_wrap_rows(self):
        box = TestBox(
            TestItem(width="50%", height=10),
            TestItem(width="50%", height=10),
            TestItem(width="100%", height=10),
            TestItem(width="50%", height=10),
            width="100%",
            flex_wrap=FlexWrap.NoWrap,
            avail_width=100,
            avail_height=100
        )
        self.assertWrap(box, 100, 10)
        self.assertFalse(box.split(100, 15))

    def test_no_split_wrap_columns(self):
        box = TestBox(
            TestItem(width="50%", height=10),
            TestItem(width="50%", height=10),
            TestItem(width="50%", height=10),
            TestItem(width="50%", height=10),
            width="100%",
            flex_wrap=FlexWrap.Wrap,
            flex_direction=FlexDirection.Column,
            avail_width=100,
            avail_height=20
        )
        self.assertWrap(box, 100, 20)
        self.assertFalse(box.split(100, 15))




