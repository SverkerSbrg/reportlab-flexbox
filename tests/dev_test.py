from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib import pagesizes

from datetime import datetime
from itertools import chain

from reportlab.platypus import KeepTogether

from flexbox import AlignContent, AlignItems, FlexBox, FlexDirection, FlexItem, FlexParagraph, FlexWrap, JustifyContent


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


doc = TestDoc(filename="test_%s.pdf" % datetime.now().strftime("%Y%m%d_%H%M%S"), pageTemplates=[TestPage()])

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
            FlexItem(
                width=width or w,
                height=height or h,
                background_color=item_color,
                margin=spacing / 2
            )
        )

    return items


h1 = ParagraphStyle("H1", fontSize=20, leading=20)
h2 = ParagraphStyle("H2", fontSize=12)


class TestBox(FlexBox):
    def wrap(self, avail_width, avail_height):
        super().wrap(avail_width, avail_height)

        return self.width, self.height


def demo():
    doc.build(flowables=[
        FlexParagraph("AlignContent", h1, margin_bottom=spacing),
        FlexBox(
            *list(
                FlexBox(
                    FlexParagraph(str(align_content), h2, margin_bottom=spacing / 2, width="100%"),
                    TestBox(
                        *list(chain(*(demo_items(height="20%", width="33%") for i in range(0, 2)))),
                        width="100%",
                        height=150,
                        background_color=container_color,
                        padding=spacing / 2,
                        align_content=align_content,
                        margin_bottom=spacing / 2
                    ),
                    flex_direction=FlexDirection.Row,
                    flex_wrap=FlexWrap.Wrap,
                    padding=spacing / 2,
                    width="50%"
                    # border_thickness=0.5
                ) for align_content in AlignContent
            ),
            flex_direction=FlexDirection.Row,
            width="100%",
            flex_wrap=FlexWrap.Wrap,
            margin=-spacing / 2
            # border_thickness=0.5

        ),
        KeepTogether(
            flowables=[
                FlexParagraph("AlignItems", h1, margin_bottom=spacing, width="100%"),
                FlexBox(
                    *list(
                        FlexBox(
                            FlexParagraph(str(align_items), h2, margin_bottom=spacing / 2, margin_left=spacing / 2),
                            FlexBox(
                                *demo_items(width="25%"),
                                height=120,
                                background_color=container_color,
                                padding=spacing / 2,
                                align_items=align_items,
                                margin=spacing / 2,
                                margin_top=0
                            ),
                            flex_direction=FlexDirection.Column,
                            width="50%"
                        ) for align_items in AlignItems
                    ),
                    width="100%",
                    flex_direction=FlexDirection.Row,
                    padding=spacing / 2,
                    margin=-spacing
                ),
            ]
        ),

        FlexBox(
            FlexParagraph("JustifyContent", h1, margin_bottom=spacing),
            *list(
                FlexBox(
                    FlexParagraph(str(justify_content), h2, margin_bottom=spacing / 2),
                    FlexBox(
                        *demo_items(height="100%"),
                        width="100%",
                        height=50,
                        background_color=container_color,
                        padding=spacing / 2,
                        justify_content=justify_content,
                        margin_bottom=spacing
                    ),
                    flex_direction=FlexDirection.Column
                ) for justify_content in JustifyContent
            ),
            flex_direction=FlexDirection.Column,
            width="100%",
            flex_wrap=FlexWrap.NoWrap,
            keep_together=True
        )
    ])


def test():
    doc.build(flowables=[
        FlexBox(
            *demo_items(height="100%"),
            width="100%",
            height=50,
            background_color=container_color,
            padding=spacing / 2,
            justify_content=JustifyContent.SpaceBetween,
            margin_bottom=spacing
        )
    ])


demo()
