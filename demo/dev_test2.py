from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib import pagesizes

from datetime import datetime
from itertools import chain

from reportlab.platypus import KeepTogether

# from flexbox import AlignContent, AlignItems, FlexBox, FlexDirection, FlexItem, FlexParagraph, FlexWrap, JustifyContent
from flexbox2.flex import FlexBox2, FlexItem2
from flexbox2.measurement import FlexMeasurement2
from flexbox2.options import AlignContent2, FlexDirection2, FlexWrap2, AlignItems2


class TestPage(PageTemplate):
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


class TestDoc(BaseDocTemplate):
    pass


doc = TestDoc(filename="tests/test_%s.pdf" % datetime.now().strftime("%Y%m%d_%H%M%S"), pageTemplates=[TestPage()])

item_color = HexColor(0xe77f24)
container_color = HexColor(0x88499c)
spacing = 6


def demo_items(height=None, width=None):
    items = []
    for w, h in (
            ("10%", "70%"),
            ("15%", "20%"),
            ("30%", "50%"),
            ("10%", "100%"),
    ):
        items.append(
            FlexItem2(
                width=width or w,
                height=height or h,
                background_color=item_color,
                margin=spacing / 2
            )
        )

    return items


h1 = ParagraphStyle("H1", fontSize=20, leading=20)
h2 = ParagraphStyle("H2", fontSize=12)





def demo():
    print(doc.build(flowables=[
        # FlexParagraph("AlignContent", h1, margin_bottom=spacing),
        # FlexBox2(
        #     FlexItem2(width=100, height=70, margin=1, background_color=item_color),
        #     FlexItem2(width=150, height=50, margin=1, background_color=item_color),
        #     # FlexItem2(width=50, height=50, margin=spacing, background_color=item_color),
        #     # padding=spacing,
        #     background_color=container_color,
        #     flex_direction=FlexDirection2.Row2,
        #     # width=100,
        #     # height=100,
        #     flex_wrap=FlexWrap2.NoWrap2
        # ),
        FlexBox2(
            FlexItem2(width=20, height=10, margin=1, background_color=item_color, align_self=AlignItems2.FlexStart),
            FlexItem2(width=20, height=10, margin=1, background_color=item_color, align_self=AlignItems2.FlexCenter),
            FlexItem2(width=20, height=10, margin=1, background_color=item_color, align_self=AlignItems2.FlexEnd),
            FlexItem2(width=20, height=10, margin=1, background_color=item_color, align_self=AlignItems2.FlexStart),
            FlexItem2(width=20, height=10, margin=1, background_color=item_color, align_self=AlignItems2.FlexCenter),
            FlexItem2(width=20, height=10, margin=1, background_color=item_color, align_self=AlignItems2.FlexEnd),
            # FlexItem2(width=50, height=50, margin=spacing, background_color=item_color),
            # padding=spacing,
            background_color=container_color,
            flex_direction=FlexDirection2.Row2,
            flex_wrap=FlexWrap2.Wrap2,
            width=60,
            height=60,
            # width=100,
            # height=100,
        )
    ]))


demo()
