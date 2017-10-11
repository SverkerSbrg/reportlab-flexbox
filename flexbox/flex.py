from fortnum import FortnumDescriptor
from reportlab.lib.colors import HexColor
from reportlab.platypus import Flowable, Paragraph

from flexbox.color import ColorDescriptor
from flexbox.measurement import FlexMeasurementDescriptor, FlexMeasurement, FlexFrameDescriptor
from flexbox.options import FlexDirection, JustifyContent, AlignItems, AlignContent, FlexWrap, Stretch


class FlexItem(Flowable):
    min_width = FlexMeasurementDescriptor()
    flex_width = FlexMeasurementDescriptor()
    max_width = FlexMeasurementDescriptor()
    
    min_height = FlexMeasurementDescriptor()
    flex_height = FlexMeasurementDescriptor()
    max_height = FlexMeasurementDescriptor()

    background_color = ColorDescriptor()
    border_color = ColorDescriptor()

    margin = FlexFrameDescriptor()
    border = FlexFrameDescriptor()
    padding = FlexFrameDescriptor()

    def __init__(self, min_width=None, width=None, max_width=None, min_height=None, height=None, max_height=None,
                 margin=None, border=None, padding=None, background_color=None, border_color=None, align_self=None):
        super().__init__()
        
        self.min_width = min_width
        self.flex_width = width
        self.max_width = max_width
        
        self.min_height = min_height
        self.flex_height = height
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
        for measurement in (self.min_width, self.flex_width, self.max_width):
            measurement.base = avail_width
        for measurement in (self.min_height, self.flex_height, self.max_height):
            measurement.base = avail_height

        width = float(FlexMeasurement.min(self.max_width, self.flex_width) or avail_width)
        height = float(FlexMeasurement.min(self.max_height, self.flex_height) or avail_height)

        frames = (self.margin, self.border, self.padding)
        for frame in frames:
            frame.width_base = width
            frame.height_base = height

        frame_width = float(self.padding.width + self.margin.width + self.border.width)
        frame_height = float(self.padding.height + self.margin.height + self.border.height)

        content_width, content_height = self.wrap_content(
            width - frame_width,
            height - frame_height
        )

        if not self.flex_width:
            width_base = (content_width + sum(f.width.static for f in frames))/(1 - sum(f.height.relative for f in frames))
            for frame in frames:
                frame.width_base = width_base

            width = content_width + sum(float(f.width) for f in frames)
        if not self.flex_height:
            height_base = (content_height + sum(f.height.static for f in frames))/(1 - sum(f.height.relative for f in frames))
            for frame in frames:
                frame.height_base = height_base

            height = content_height + sum(float(f.height) for f in frames)

        if self.min_width:
            width = max(width, float(self.min_width))
        if self.max_width:
            width = min(width, float(self.max_width))

        if self.min_height:
            height = max(height, float(self.min_height))
        if self.max_height:
            height = min(height, float(self.max_height))

        for frame in frames:
            frame.width_base = width
            frame.height_base = height

        self.width = width
        self.height = height
        self.content_width = content_width
        self.content_height = content_height

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
            self.width - float(self.margin.width),
            self.height - float(self.margin.height)
        )
        self.canv.restoreState()

        self.canv.saveState()
        self.canv.translate(
            float(self.margin.left + self.padding.left + self.border.left),
            float(self.margin.bottom + self.padding.bottom + self.border.bottom)
        )
        self.draw_content(
            self.width - float(self.margin.width + self.padding.width + self.border.width),
            self.height - float(self.margin.height + self.padding.height + self.border.height),
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


class FlexBox(FlexItem):
    flex_direction = FortnumDescriptor("flex_direction", FlexDirection, default=FlexDirection.Row2)
    justify_content = FortnumDescriptor("justify_content", JustifyContent, default=JustifyContent.FlexStart)
    align_items = FortnumDescriptor("align_items", AlignItems, default=AlignItems.FlexStart)
    align_content = FortnumDescriptor("align_content", AlignContent, default=AlignContent.Stretch)
    flex_wrap = FortnumDescriptor("flex_wrap", FlexWrap, default=FlexWrap.NoWrap)

    def __init__(self, *flex_items, flex_direction=None, justify_content=None, align_content=None, align_items=None,
                  flex_wrap=None, keep_together=None,  **kwargs):

        self.items = flex_items
        self.rows = None

        self.flex_direction = flex_direction
        self.justify_content = justify_content
        self.align_items = align_items
        self.align_content = align_content
        self.flex_wrap = flex_wrap
        self.keep_together = keep_together if keep_together is not None else False

        super().__init__(**kwargs)

    def wrap_content(self, avail_width, avail_height):
        if not self.items:
            return 0, 0

        for item in self.items:
            item.wrap(avail_width, avail_height)

        if self.flex_wrap == FlexWrap.Wrap:
            if self.flex_direction == FlexDirection.Row2:
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

        if self.flex_direction == FlexDirection.Row2:
            for row in self.rows:
                row.width, row.height = sum(widths(row)), max(heights(row))

            content_width, content_height = max(widths(self.rows)), sum(heights(self.rows))
        else:
            for row in self.rows:
                row.width, row.height = max(widths(row)), sum(heights(row))

            content_width, content_height = sum(widths(self.rows)), max(heights(self.rows))

        return content_width, content_height

    def draw_content(self, avail_width, avail_height, requested_width, requested_height):
        if self.flex_direction == FlexDirection.Row2:
            row_heights = heights(self.rows)
            if self.align_content == AlignContent.Stretch:
                row_heights = tuple(AlignContent.Stretch.stretch(row_heights, avail_height))

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
            if self.align_content == AlignContent.Stretch:
                col_widths = tuple(AlignContent.Stretch.stretch(col_widths, avail_width))
            for col, x, col_width in zip(self.rows, self.align_content.points(col_widths, avail_width), col_widths):
                for item, y in zip(col, self.justify_content.points(heights(col), avail_height)):
                    align_item = getattr(item, "align_self", None) or self.align_items
                    item.drawOn(self.canv, x + align_item.point(float(item.width), col_width),
                                avail_height - float(item.height) - y, )




