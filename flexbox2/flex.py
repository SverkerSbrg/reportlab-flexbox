from reportlab.lib.colors import HexColor
from reportlab.platypus import Flowable

from flexbox2.measurement import Measurement2Descriptor, FlexMeasurement2, FrameDescriptor
from flexbox2.options import FlexDirection2, JustifyContent2, AlignItems2, AlignContent2, FlexWrap2, Stretch2


class FlexItem2(Flowable):
    min_width = Measurement2Descriptor()
    width = Measurement2Descriptor()
    max_width = Measurement2Descriptor()
    
    min_height = Measurement2Descriptor()
    height = Measurement2Descriptor()
    max_height = Measurement2Descriptor()

    background_color = None
    border_color = None

    margin = FrameDescriptor()
    border = FrameDescriptor()
    padding = FrameDescriptor()

    def __init__(self, min_width=None, width=None, max_width=None, min_height=None, height=None, max_height=None,
                 margin=None, border=None, padding=None, background_color=None, border_color=None, align_self=None):
        super().__init__()
        
        self.min_width = min_width
        self.width = width
        self.max_width = max_width
        
        self.min_height = min_height
        self.height = height
        self.max_height = max_height

        self.margin = margin
        self.border = border
        self.padding = padding

        self.background_color = background_color
        self.border_color = border_color

        self.content_width = None
        self.content_height = None

        self.align_self = align_self

    def wrap(self, avail_width, avail_height):
        for measurement in (self.min_width, self.width, self.max_width):
            measurement.base = avail_width
        for measurement in (self.min_height, self.height, self.max_height):
            measurement.base = avail_height

        width = FlexMeasurement2.max(self.width, self.min_width)
        if width:
            width = FlexMeasurement2.min(width, self.max_width)
        height = FlexMeasurement2.max(self.height, self.min_height)
        if height:
            height = FlexMeasurement2.min(height, self.max_height)

        self.padding.width_base = width or 0
        self.margin.width_base = width or 0
        self.border.width_base = width or 0

        self.padding.height_base = height or 0
        self.margin.height_base = height or 0
        self.border.height_base = height or 0

        frame_width = self.padding.width + self.margin.width + self.border.width
        frame_height = self.padding.height + self.margin.height + self.border.height

        content_width, content_height = self.wrap_content(
            width - frame_width if width else 0,
            height - frame_height if height else 0
        )

        if width is None or height is None:
            if width is None:
                width = FlexMeasurement2.min(content_width + frame_width)
            if height is None:
                height = FlexMeasurement2.min(content_height + frame_height)

            content_width, content_height = self.wrap_content(width - frame_width, height - frame_height)

        self.content_width = content_width
        self.content_height = content_height

        self.width = width
        self.width.base = 0
        self.height = height
        self.height.base = 0

        return width, height

    def wrap_content(self, avail_width, avail_height):
        return 0, 0

    def draw_background(self, background_width, background_height):
        top = float(self.border.top)
        right = float(self.border.right)
        bottom = float(self.border.bottom)
        left = float(self.border.left)

        if self.background_color:
            self.canv.setFillColor(self.background_color)

            self.canv.rect(
                bottom/2, left/2, background_width-right/2-left/2, background_height-top/2-bottom/2, stroke=False, fill=True
            )

        self.canv.setStrokeColor(self.border_color or HexColor(0x000000))

        if top:
            self.canv.setLineWidth(top)
            self.canv.line(0, background_height - top/2, background_width, background_height - top/2)
        if right:
            self.canv.setLineWidth(right)
            self.canv.line(background_width - right/2, background_height, background_width - right/2, 0)
        if bottom:
            self.canv.setLineWidth(bottom)
            self.canv.line(background_width, bottom/2, 0, bottom/2)
        if left:
            self.canv.setLineWidth(left)
            self.canv.line(left/2, 0, left/2, background_height)

    def draw(self):
        self.canv.saveState()
        self.canv.translate(
            float(self.margin.left),
            float(self.margin.bottom)
        )
        self.draw_background(
            self.width - self.margin.width,
            self.height - self.margin.height
        )
        self.canv.restoreState()

        self.canv.saveState()
        self.canv.translate(
            self.margin.left + self.padding.left + float(self.border.left),
            self.margin.bottom + self.padding.bottom + float(self.border.bottom)
        )
        self.draw_content(
            self.width - self.margin.width - self.padding.width - self.border.width,
            self.height - self.margin.height - self.padding.height - self.border.height,
            self.content_width,
            self.content_height
        )
        self.canv.restoreState()

    def draw_content(self, avail_width, avail_height, requested_width, requested_height):
        pass


def widths(items):
    return tuple(float(getattr(item, "width", 0)) for item in items)


def heights(items):
    return tuple(float(getattr(item, "height", 0)) for item in items)


class FlexRow(list):
    width = None
    height = None


class FlexBox2(FlexItem2):
    def __init__(self, *flex_items, flex_direction=None, justify_content=None, align_content=None, align_items=None,
                  flex_wrap=None, keep_together=None,  **kwargs):

        self.items = flex_items
        self.rows = None

        self.flex_direction = flex_direction or FlexDirection2.Row2
        self.justify_content = justify_content or JustifyContent2.FlexStart
        self.align_items = align_items or AlignItems2.FlexStart
        self.align_content = align_content or AlignContent2.Stretch
        self.flex_wrap = flex_wrap or FlexWrap2.NoWrap2
        self.keep_together = keep_together if keep_together is not None else False

        super().__init__(**kwargs)

        self._validate_configuration()

    def _validate_configuration(self):
        for attr, collection in (
                ("flex_direction", FlexDirection2),
                ("justify_content", JustifyContent2),
                ("align_content", AlignContent2),
                ("align_items", AlignItems2),
                ("flex_wrap", FlexWrap2),
        ):
            value = getattr(self, attr)
            if value not in collection:
                raise ValueError("'%s' is not av valid value for %s.%s. Try [%s]" % (
                    value, type(self).__name__, attr,
                    ", ".join(("%s.%s" % (collection.__name__, item.__name__) for item in collection))
                ))

    def wrap_content(self, avail_width, avail_height):
        if not self.items:
            return 0, 0

        for item in self.items:
            item.wrap(avail_width, avail_height)

        if self.flex_wrap == FlexWrap2.Wrap2:
            if self.flex_direction == FlexDirection2.Row2:
                available, lengths = avail_width, widths(self.items)
            else:
                available, lengths = avail_height, heights(self.items)

            self.rows = []
            row = FlexRow()
            row_length = 0
            for item, length in zip(self.items, lengths):
                row_length += length
                if row_length > available and row:
                    self.rows.append(row)
                    row = FlexRow()
                    row_length = length
                row.append(item)
            self.rows.append(row)
        else:
            self.rows = [FlexRow(self.items)]

        if self.flex_direction == FlexDirection2.Row2:
            for row in self.rows:
                row.width, row.height = sum(widths(row)), max(heights(row))

            content_width, content_height = max(widths(self.rows)), sum(heights(self.rows))
        else:
            for row in self.rows:
                row.width, row.height = max(widths(row)), sum(heights(row))

            content_width, content_height = sum(widths(self.rows)), max(heights(self.rows))

        return content_width, content_height

    def draw_content(self, avail_width, avail_height, requested_width, requested_height):
        if self.flex_direction == FlexDirection2.Row2:
            row_heights = heights(self.rows)
            if self.align_content == AlignContent2.Stretch:
                row_heights = tuple(AlignContent2.Stretch.stretch(row_heights, avail_height))

            for row, y, row_height in zip(self.rows, self.align_content.points(row_heights, avail_height), row_heights):
                y = avail_height - y
                for item, x in zip(row, self.justify_content.points(widths(row), avail_width)):
                    align_item = getattr(item, "align_self", None) or self.align_items

                    item.drawOn(
                        self.canv,
                        x,
                        y - float(item.height) - align_item.point(float(item.height), row_height)
                    )
        else:
            col_widths = widths(self.rows)
            if self.align_content == AlignContent2.Stretch:
                col_widths = tuple(AlignContent2.Stretch.stretch(col_widths, avail_width))
            for col, x, col_width in zip(self.rows, self.align_content.points(col_widths, avail_width), col_widths):
                for item, y in zip(col, self.justify_content.points(heights(col), avail_height)):
                    align_item = getattr(item, "align_self", None) or self.align_items
                    item.drawOn(self.canv, x + align_item.point(float(item.width), col_width),
                                avail_height - float(item.height) - y, )


class TestItem(FlexItem2):
    def wrap_content(self, avail_width, avail_height):
        return 100, 100

    def draw_content(self, avail_width, avail_height, requested_width, requested_height):
        self.canv.setStrokeColor(HexColor(0xFF0000))
        self.canv.rect(0, 0, requested_width, requested_height)
        self.canv.setLineWidth(10)
        self.canv.line(0, 0, requested_width, requested_height)

        self.canv.setStrokeColor(HexColor(0x000000))
        self.canv.setLineWidth(1)
        self.canv.line(0, 0, requested_width, requested_height)

