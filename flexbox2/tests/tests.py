import unittest

from flexbox2.flex import FlexItem
from flexbox2.measurement import Measurement2Descriptor


class TestItem(FlexItem):
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