from weakref import WeakKeyDictionary

from reportlab.lib.colors import Color
from reportlab.platypus import Flowable
from reportlab.platypus import Paragraph

from flexbox.measurement import BoundMeasurement, Frame, FlexMeasurement
from flexbox.options import FlexDirection, JustifyContent, AlignItems, FlexWrap, AlignContent


def _(*options):
    for option in options:
        if option is not None:
            return option
    return None


class FlexItem(Flowable):
    # Measurement
    min_width = None
    base_width = None
    max_width = None
    flex_width = None

    min_height = None
    base_height = None
    max_height = None
    flex_height = None

    align_self = None

    # Graphics
    background_color = None
    border_thickness = 0
    border_radius = 0
    border_color = Color(0, 0, 0, 1)

    margin = 0
    margin_left = None
    margin_right = None
    margin_top = None
    margin_bottom = None

    padding = 0
    padding_left = None
    padding_right = None
    padding_top = None
    padding_bottom = None

    def __init__(self, min_width=None, width=None, max_width=None, min_height=None, height=None, max_height=None,
                 align_self=None, background_color=None, border_thickness=0, border_radius=0, border_color=None,
                 margin=None, margin_left=None, margin_right=None, margin_top=None, margin_bottom=None, padding=None,
                 padding_left=None, padding_right=None, padding_top=None, padding_bottom=None):
        super().__init__()

        self.flex_width = BoundMeasurement(
            base=_(width, self.base_width),
            min=_(min_width, self.min_width),
            max=_(max_width, self.max_width)
        )

        self.flex_height = BoundMeasurement(
            base=_(height, self.base_height),
            min=_(min_height, self.min_height),
            max=_(max_height, self.max_height)
        )

        self.align_self = _(align_self, self.align_self)

        self.background_color = background_color or self.background_color
        self.border_thickness = border_thickness or self.border_thickness
        self.border_radius = border_radius or self.border_radius
        self.border_color = border_color or self.border_color

        self.margin_frame = Frame(
            _(margin_top, self.margin_top),
            _(margin_right, self.margin_right),
            _(margin_bottom, self.margin_bottom),
            _(margin_left, self.margin_left),
            default=_(margin, self.margin)
        )

        self.padding_frame = Frame(
            _(padding_top, self.padding_top),
            _(padding_right, self.padding_right),
            _(padding_bottom, self.padding_bottom),
            _(padding_left, self.padding_left),
            default=_(padding, self.padding)
        )

    def wrap(self, avail_width, avail_height):
        width = self.flex_width.length(avail_width)
        height = self.flex_height.length(avail_height)

        frame_width = self.margin_frame.width + self.padding_frame.width + self.border_thickness * 2
        frame_height = self.margin_frame.height + self.padding_frame.height + self.border_thickness * 2

        content_width, content_height = self.wrap_content(
            ((
                 self.flex_width.base or self.flex_width.max or FlexMeasurement(static=avail_width)
             ) - frame_width).length(avail_width),
            ((
                 self.flex_height.base or self.flex_height.max or FlexMeasurement(static=avail_height)
             ) - frame_height).length(avail_height),
        )

        self.width = max(width, frame_width.parent_length(content_width))
        self.height = max(height, frame_height.parent_length(content_height))

        return self.width, self.height

    def wrap_content(self, avail_width, avail_height):
        return 0, 0

    def draw(self):
        self.canv.saveState()
        self.canv.translate(
            self.margin_frame.left.length(self.width),
            self.margin_frame.bottom.length(self.height)
        )
        self.draw_background(
            self.width - self.margin_frame.width.length(self.width),
            self.height - self.margin_frame.height.length(self.height),
        )
        self.canv.restoreState()

        self.canv.saveState()
        self.canv.translate(
            (self.margin_frame.left + self.padding_frame.left + self.border_thickness).length(self.width),
            (self.margin_frame.bottom + self.padding_frame.bottom + self.border_thickness).length(self.height),
        )
        self.draw_content(
            self.width - (self.margin_frame.width + self.padding_frame.width + (self.border_thickness * 2)).length(
                self.width),
            self.height - (self.margin_frame.height + self.padding_frame.height + (self.border_thickness * 2)).length(
                self.height)
        )
        self.canv.restoreState()

    def draw_background(self, background_width, background_height):
        if self.background_color or self.border_thickness:
            self.canv.saveState()

            self.canv.setStrokeColor(self.border_color)
            if self.border_thickness:
                self.canv.setLineWidth(self.border_thickness)
            if self.background_color:
                self.canv.setFillColor(self.background_color)

            self.canv.roundRect(
                0 + self.border_thickness / 2,
                0 + self.border_thickness / 2,
                background_width - self.border_thickness,
                background_height - self.border_thickness,
                self.border_radius,
                fill=bool(self.background_color),
                stroke=bool(self.border_thickness),
            )

            self.canv.restoreState()

    def draw_content(self, content_width, content_height):
        pass


class _FlexRow(list):
    def __init__(self, flex_direction, items=None):
        super().__init__(items or [])

        self.flex_direction = flex_direction

    @property
    def width(self):
        return self.flex_direction.width(self)

    @property
    def height(self):
        return self.flex_direction.height(self)


class FlexBox(FlexItem):
    flex_direction = FlexDirection.Row
    justify_content = JustifyContent.FlexStart
    align_items = AlignItems.FlexStart
    align_content = AlignContent.FlexStart
    flex_wrap = FlexWrap.Wrap
    keep_together = False

    def __init__(self, *flex_items, flex_direction=None, justify_content=None, align_content=None, align_items=None,
                 flex_wrap=None, keep_together=None, **kwargs):
        self.items = flex_items

        self.flex_direction = flex_direction or self.flex_direction
        self.justify_content = justify_content or self.justify_content
        self.align_content = align_content or self.align_content
        self.align_items = align_items or self.align_items
        self.flex_wrap = flex_wrap or self.flex_wrap
        self.keep_together = keep_together if keep_together is not None else self.keep_together

        self._rows = []

        super().__init__(**kwargs)

        # Store kwargs for easy duplication in split method.
        self._kwargs = kwargs
        self._kwargs.update({
            "flex_direction": flex_direction,
            "justify_content": justify_content,
            "align_content": align_content,
            "align_items": align_items,
            "flex_wrap": flex_wrap,
            "keep_together": keep_together
        })

        self._validate_configuration()

    def _validate_configuration(self):
        for attr, collection in (
                ("flex_direction", FlexDirection),
                ("justify_content", JustifyContent),
                ("align_content", JustifyContent),
                ("align_items", AlignItems),
                ("flex_wrap", FlexWrap),
        ):
            value = getattr(self, attr)
            if value not in collection:
                raise ValueError("'%s' is not av valid value for %s.%s. Try [%s]" % (
                    value, type(self).__name__, attr,
                    ", ".join(("%s.%s" % (collection.__name__, item.__name__) for item in collection))
                ))

    def wrap_content(self, avail_width, avail_height):
        for item in self.items:
            item.wrap(avail_width, avail_height)

        rows = []
        if self.flex_wrap == FlexWrap.Wrap:
            if self.flex_direction == FlexDirection.Row:
                limit, attr = (avail_width, "width")
            else:
                limit, attr = (avail_height, "height")

            row = _FlexRow(self.flex_direction)
            length = 0

            for item in self.items:
                length += getattr(item, attr)

                # Atleast one item in every row, this prevents items with dimensions
                # larger then the container from creating empty rows.
                if length > limit and row:
                    rows.append(row)
                    row = _FlexRow(self.flex_direction)
                    length = getattr(item, attr)

                row.append(item)
            rows.append(row)
        else:
            rows.append(_FlexRow(self.flex_direction, items=self.items))

        self._rows = rows

        width = self.flex_direction.container_width(rows)
        height = self.flex_direction.container_height(rows)

        return width, height

    def draw_content(self, content_width, content_height):
        rows = self._rows

        if self.flex_direction == FlexDirection.Row:
            for row, y in zip(rows, self.align_content.points(rows, content_height, lambda r: r.height)):
                y = content_height - y

                for item, x in zip(row, self.justify_content.points(self.items, content_width, lambda i: i.width)):
                    item.drawOn(
                        self.canv,
                        x,
                        y - item.height - (item.align_self or self.align_items).point(item, row.height,
                                                                                      lambda i: i.height)
                    )
        else:
            for row, x in zip(rows, self.align_content.points(rows, content_width, lambda r: r.width)):
                for item, y in zip(row, self.justify_content.points(self.items, content_height, lambda i: i.height)):
                    item.drawOn(
                        self.canv,
                        x + (item.align_self or self.align_items).point(item, row.width, lambda i: i.width),
                        content_height - item.height - y
                    )

    def split(self, avail_width, avail_height):
        if self.keep_together or self.height < avail_height:
            return []

        avail_height -= (self.margin_frame.height + self.padding_frame.height + self.border_thickness * 2).length(
            self.height)
        first = []
        second = []
        if self.flex_direction == FlexDirection.Column:
            for row in self._rows:
                height = 0
                for item in row:
                    height += item.height
                    (second if height > avail_height else first).append(item)
        else:
            height = 0
            for row in self._rows:
                height += row.height
                (second if height > avail_height else first).extend(row)

        if not (first and second):
            return []

        return [
            FlexBox(*first, **self._kwargs),
            FlexBox(*second, **self._kwargs)
        ]


class FlexFlowable(FlexItem):
    flowable = None

    vertical_align = AlignItems.FlexCenter
    horizontal_align = AlignItems.FlexCenter

    _flowable_width = None
    _flowable_height = None

    def __init__(self, flowable, vertical_align=None, horizontal_align=None, **kwargs):
        super().__init__(**kwargs)

        self.flowable = flowable
        self.vertical_align = vertical_align or self.vertical_align
        self.horizontal_align = horizontal_align or self.horizontal_align

    def wrap_content(self, avail_width, avail_height):
        self._flowable_width, self._flowable_height = self.flowable.wrap(avail_width, avail_height)
        return self._flowable_width, self._flowable_height

    def draw_content(self, content_width, content_height):
        self.flowable.drawOn(
            self.canv,
            self.vertical_align.point(self.flowable, content_width, lambda i: self._flowable_width),
            self.horizontal_align.point(self.flowable, content_height, lambda i: self._flowable_height)
        )


class FlexParagraph(FlexFlowable):
    def __init__(self, text, style, **kwargs):
        super().__init__(
            Paragraph(text, style),
            **kwargs
        )

    def draw_content(self, content_width, content_height):
        super().draw_content(content_width, content_height)
