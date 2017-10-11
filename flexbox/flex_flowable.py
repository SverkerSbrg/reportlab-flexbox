from fortnum import FortnumDescriptor
from reportlab.platypus import Paragraph, Image

from flexbox.options import AlignItems
from flexbox.flex import FlexItem

from PIL import Image as PILImage


class FlexFlowable(FlexItem):
    flowable = None

    vertical_align = FortnumDescriptor("vertical_align", AlignItems, default=AlignItems.FlexCenter)
    horizontal_align = FortnumDescriptor("horizontal_align", AlignItems, default=AlignItems.FlexCenter)

    def __init__(self, flowable, vertical_align=None, horizontal_align=None, **kwargs):
        super().__init__(**kwargs)

        self.flowable = flowable
        self.vertical_align = vertical_align or self.vertical_align
        self.horizontal_align = horizontal_align or self.horizontal_align

    def wrap_content(self, avail_width, avail_height):
        return self.flowable.wrap(avail_width, avail_height)

    def draw_content(self, avail_width, avail_height, requested_width, requested_height):
        self.flowable.drawOn(
            self.canv,
            self.vertical_align.point(requested_width, avail_width),
            self.horizontal_align.point(requested_height, avail_height)
        )


class FlexParagraph(FlexFlowable):
    def __init__(self, text, style, **kwargs):
        super().__init__(
            Paragraph(text, style),
            **kwargs
        )


class FlexImage(FlexFlowable):
    def __init__(self, image, **kwargs):
        self.image = image

        with PILImage.open(self.image) as img:
            img_width, img_height = img.size
            self.aspect = img_height / img_width

        super().__init__(None, **kwargs)

    def wrap_content(self, avail_width, avail_height):
        height = avail_height
        width = height / self.aspect

        if width > avail_width:
            height = height * avail_width / width
            width = avail_width

        self.flowable = Image(self.image, width, height)

        return width, height
