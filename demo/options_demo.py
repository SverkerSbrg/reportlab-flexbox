from os.path import dirname, join
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import KeepTogether

from demo.common import DemoDocTemplate, h1, spacing, DemoFlexBox, DemoFlexItem, h2
from flexbox import FlexBox, FlexParagraph, FlexWrap, FlexDirection, JustifyContent, AlignItems, AlignContent
from flexbox.flex_flowable import FlexImage

wrap = FlexBox(
    FlexParagraph(str(FlexWrap.NoWrap), h2, padding=[spacing / 2, spacing / 2, 0]),
    DemoFlexBox(
        DemoFlexItem(width="35%", height=25),
        DemoFlexItem(width="15%", height=25),
        DemoFlexItem(width="30%", height=25),
        DemoFlexItem(width="20%", height=25),
        DemoFlexItem(width="25%", height=25),
        DemoFlexItem(width="15%", height=25),
        width="70%",
        flex_wrap=FlexWrap.NoWrap
    ),
    FlexParagraph(str(FlexWrap.Wrap), h2, padding=[spacing / 2, spacing / 2, 0]),
    DemoFlexBox(
        DemoFlexItem(width="35%", height=25),
        DemoFlexItem(width="15%", height=25),
        DemoFlexItem(width="30%", height=25),
        DemoFlexItem(width="20%", height=25),
        DemoFlexItem(width="25%", height=25),
        DemoFlexItem(width="15%", height=25),
        width="70%",
        flex_wrap=FlexWrap.Wrap
    ),
    flex_direction=FlexDirection.Column,
    width="100%",
    margin=(0, -spacing / 2)
)

justify_content = FlexBox(
    *list(FlexBox(
        FlexParagraph(str(justify_content), h2, padding=[spacing / 2, spacing / 2, 0]),
        DemoFlexBox(
            DemoFlexItem(width="30%", height=25),
            DemoFlexItem(width="10%", height=25),
            DemoFlexItem(width="20%", height=25),
            width="100%",
            justify_content=justify_content
        ),
        flex_direction=FlexDirection.Column,
        width="50%"
    ) for justify_content in JustifyContent
          ),
    flex_wrap=FlexWrap.Wrap,
    width="100%",
    margin=(0, -spacing / 2)
)

align_items = FlexBox(
    *list(FlexBox(
        FlexParagraph(str(align_items), h2, padding=[spacing / 2, spacing / 2, 0]),
        DemoFlexBox(
            DemoFlexItem(width="25%", height="100%"),
            DemoFlexItem(width="25%", height="35%"),
            DemoFlexItem(width="25%", height="60%"),
            DemoFlexItem(width="25%", height="45%"),
            width="100%",
            height=100,
            align_items=align_items
        ),
        flex_direction=FlexDirection.Column,
        width="33.3%"
    ) for align_items in AlignItems),
    flex_wrap=FlexWrap.Wrap,
    width="100%",
    margin=(0, -spacing / 2)
)

align_content = FlexBox(
    *list(FlexBox(
        FlexParagraph(str(align_content), h2, padding=[spacing / 2, spacing / 2, 0]),
        DemoFlexBox(
            DemoFlexItem(width="25%", height=20),
            DemoFlexItem(width="50%", height=20),
            DemoFlexItem(width="25%", height=20),
            DemoFlexItem(width="20%", height=20),
            DemoFlexItem(width="20%", height=20),
            DemoFlexItem(width="25%", height=20),
            DemoFlexItem(width="35%", height=20),
            DemoFlexItem(width="40%", height=20),
            DemoFlexItem(width="15%", height=20),
            width="100%",
            height=100,
            align_content=align_content,
            flex_wrap=FlexWrap.Wrap
        ),
        flex_direction=FlexDirection.Column,
        width="33.3%"
    ) for align_content in AlignContent),
    flex_wrap=FlexWrap.Wrap,
    width="100%",
    margin=(0, -spacing / 2)
)


def image_path(image):
    return join(dirname(__file__), "images", image)


class TankPlate(FlexBox):
    def __init__(self, equipment, chemical, volume):
        large_text = ParagraphStyle("tank_plate_large", fontSize=18, leading=18, alignment=TA_CENTER)
        small_text = ParagraphStyle("tank_plate_small", fontSize=12, leading=12, alignment=TA_CENTER)
        super().__init__(
            FlexBox(
                FlexImage(image_path("GHS01.jpg"), width="20%"),
                FlexImage(image_path("GHS03.jpg"), width="20%"),
                FlexImage(image_path("GHS06.jpg"), width="20%"),
                FlexImage(image_path("GHS09.jpg"), width="20%"),
                padding=10
            ),
            FlexParagraph(equipment, large_text),
            FlexParagraph(chemical, large_text),
            FlexParagraph(
                volume,
                small_text,
                margin=(10, 0, 0),
                border=(1, 0, 0),
                border_color="#000000",
                background_color="#ff0000",
                padding=5

            ),
            border=1,
            border_color="#000000",
            width="50%",
            flex_direction=FlexDirection.Column,
            align_items=JustifyContent.FlexCenter
        )


if __name__ == "__main__":
    doc = DemoDocTemplate("options_demo", timestamp=True)
    doc.build(
        flowables=[
            FlexParagraph("Wrap", h1, padding=(spacing * 2, 0, 0)),
            wrap,
            FlexParagraph("JustifyContent", h1, padding=(spacing * 2, 0, 0)),
            justify_content,
            FlexParagraph("AlignItems", h1, padding=(spacing * 2, 0, 0)),
            align_items,
            KeepTogether(
                flowables=[
                    FlexParagraph("AlignContent", h1, padding=(spacing * 2, 0, 0)),
                    align_content,
                ]
            ),
            FlexParagraph("TankPlate", h1, padding=(spacing * 2, 0, spacing)),
            TankPlate("Cistern A2", "Acetone", "Volume 5000 [L]"),
        ]
    )
