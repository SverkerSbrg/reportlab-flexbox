from datetime import datetime

from os.path import dirname, join
from reportlab.lib import pagesizes
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageTemplate, BaseDocTemplate, Frame

from flexbox2.flex import FlexItem, FlexBox, FlexParagraph2


class DemoPage(PageTemplate):
    pagesize = pagesizes.A4
    margins = 80

    def __init__(self):
        super().__init__(
            pagesize=pagesizes.A4,
            frames=Frame(
                x1=self.margins,
                y1=self.margins,
                width=pagesizes.A4[0] - self.margins * 2,
                height=pagesizes.A4[1] - self.margins * 2,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
            )
        )


class DemoDocTemplate(BaseDocTemplate):
    def __init__(self, name, timestamp=False):
        if timestamp:
            name = "%s_%s" % (name, datetime.now().strftime("%Y%m%d_%H%M%S"))
        super().__init__(
            filename=join(dirname(__file__), "%s.pdf" % name),
            pageTemplates=[DemoPage()]
        )

item_color = HexColor(0xe77f24)
container_color = HexColor(0x88499c)
spacing = 6

h1 = ParagraphStyle("H1", fontSize=20, leading=20)
h2 = ParagraphStyle("H2", fontSize=12)


class DemoFlexItem(FlexItem):
    def __init__(self, **kwargs):
        kwargs.update(
            background_color=item_color,
            margin=spacing/2,
        )
        super().__init__(**kwargs)


class DemoFlexBox(FlexBox):
    def __init__(self, *items, **kwargs):
        kwargs.update(
            background_color=container_color,
            padding=spacing/2,
            margin=spacing/2
        )
        super().__init__(*items, **kwargs)
