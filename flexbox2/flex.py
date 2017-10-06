from reportlab.lib.colors import HexColor
from reportlab.platypus import Flowable

from flexbox import FlexDirection, JustifyContent, AlignItems, FlexWrap
from flexbox2.measurement import Measurement2Descriptor, FlexMeasurement2, FrameDescriptor


class FlexItem(Flowable):
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
                 margin=None, border=None, padding=None, background_color=None, border_color=None):
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

        self.padding.base = width or 0
        self.margin.base = width or 0
        self.border.base = width or 0

        frame_width = self.padding.width + self.margin.width + self.border.width
        frame_height = self.padding.height + self.margin.height + self.border.width

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
        self.draw_content(self.content_width, self.content_height)
        self.canv.restoreState()

    def draw_content(self, content_width, content_height):
        pass


# class FlexBox(FlexItem):
#     def __init__(self, *flex_items, flex_direction=None, justify_content=None, align_content=None, align_items=None,
#                  flex_wrap=None, keep_together=None, **kwargs):
#         self.items = flex_items
#
#         self.flex_direction = flex_direction
#         self.justify_content = justify_content
#         self.align_content = align_content
#         self.align_items = align_items
#         self.flex_wrap = flex_wrap
#         self.keep_together = keep_together
#
#         self._rows = []
#
#         super().__init__(**kwargs)
#
#         # Store kwargs for easy duplication in split method.
#         self._kwargs = kwargs
#         self._kwargs.update({
#             "flex_direction": flex_direction,
#             "justify_content": justify_content,
#             "align_content": align_content,
#             "align_items": align_items,
#             "flex_wrap": flex_wrap,
#             "keep_together": keep_together
#         })
#
#         self._validate_configuration()
#
#     def _validate_configuration(self):
#         for attr, collection in (
#                 ("flex_direction", FlexDirection),
#                 ("justify_content", JustifyContent),
#                 ("align_content", JustifyContent),
#                 ("align_items", AlignItems),
#                 ("flex_wrap", FlexWrap),
#         ):
#             value = getattr(self, attr)
#             if value not in collection:
#                 raise ValueError("'%s' is not av valid value for %s.%s. Try [%s]" % (
#                     value, type(self).__name__, attr,
#                     ", ".join(("%s.%s" % (collection.__name__, item.__name__) for item in collection))
#                 ))
#
#     def wrap_content(self, avail_width, avail_height):
#         pass


class TestItem(FlexItem):
    def wrap_content(self, avail_width, avail_height):
        return 100, 100

    def draw_content(self, content_width, content_height):
        self.canv.setStrokeColor(HexColor(0xFF0000))
        self.canv.rect(0, 0, content_width, content_height)
        self.canv.setLineWidth(10)
        self.canv.line(0, 0, content_width, content_height)

        self.canv.setStrokeColor(HexColor(0x000000))
        self.canv.setLineWidth(1)
        self.canv.line(0, 0, content_width, content_height)

