from reportlab.platypus import KeepTogether

from demo.common import DemoDocTemplate, h1, spacing, DemoFlexBox, DemoFlexItem, h2
from flexbox2.flex import FlexParagraph2, FlexBox2, FlexItem2
from flexbox2.options import AlignContent2, JustifyContent2, FlexDirection2, FlexWrap2, AlignItems2

wrap = FlexBox2(
    FlexParagraph2(str(FlexWrap2.NoWrap2), h2, padding=[spacing/2, spacing/2, 0]),
    DemoFlexBox(
        DemoFlexItem(width="35%", height=25),
        DemoFlexItem(width="15%", height=25),
        DemoFlexItem(width="30%", height=25),
        DemoFlexItem(width="20%", height=25),
        DemoFlexItem(width="25%", height=25),
        DemoFlexItem(width="15%", height=25),
        width="70%",
        flex_wrap=FlexWrap2.NoWrap2
    ),
    FlexParagraph2(str(FlexWrap2.Wrap2), h2, padding=[spacing / 2, spacing / 2, 0]),
    DemoFlexBox(
        DemoFlexItem(width="35%", height=25),
        DemoFlexItem(width="15%", height=25),
        DemoFlexItem(width="30%", height=25),
        DemoFlexItem(width="20%", height=25),
        DemoFlexItem(width="25%", height=25),
        DemoFlexItem(width="15%", height=25),
        width="70%",
        flex_wrap=FlexWrap2.Wrap2
    ),
    flex_direction=FlexDirection2.Column2,
    width="100%",
    margin=(0, -spacing/2)
)

justify_content = FlexBox2(
    *list(FlexBox2(
            FlexParagraph2(str(justify_content), h2, padding=[spacing/2, spacing/2, 0]),
            DemoFlexBox(
                DemoFlexItem(width="30%", height=25),
                DemoFlexItem(width="10%", height=25),
                DemoFlexItem(width="20%", height=25),
                width="100%",
                justify_content=justify_content
            ),
            flex_direction=FlexDirection2.Column2,
            width="50%"
        )for justify_content in JustifyContent2
    ),
    flex_wrap=FlexWrap2.Wrap2,
    width="100%",
    margin=(0, -spacing/2)
)

align_items = FlexBox2(
    *list(FlexBox2(
        FlexParagraph2(str(align_items), h2, padding=[spacing/2, spacing / 2, 0]),
        DemoFlexBox(
            DemoFlexItem(width="25%", height="100%"),
            DemoFlexItem(width="25%", height="35%"),
            DemoFlexItem(width="25%", height="60%"),
            DemoFlexItem(width="25%", height="45%"),
            width="100%",
            height=100,
            align_items=align_items
        ),
        flex_direction=FlexDirection2.Column2,
        width="33.3%"
    ) for align_items in AlignItems2),
    flex_wrap=FlexWrap2.Wrap2,
    width="100%",
    margin=(0, -spacing/2)
)

align_content = FlexBox2(
    *list(FlexBox2(
        FlexParagraph2(str(align_content), h2, padding=[spacing/2, spacing / 2, 0]),
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
            flex_wrap=FlexWrap2.Wrap2
        ),
        flex_direction=FlexDirection2.Column2,
        width="33.3%"
    ) for align_content in AlignContent2),
    flex_wrap=FlexWrap2.Wrap2,
    width="100%",
    margin=(0, -spacing/2)
)


if __name__ == "__main__":
    doc = DemoDocTemplate("options", timestamp=True)
    doc.build(
        flowables=[
            FlexParagraph2("Wrap", h1, padding=(spacing*2, 0, 0)),
            wrap,
            FlexParagraph2("JustifyContent", h1, padding=(spacing*2, 0, 0)),
            justify_content,
            FlexParagraph2("AlignItems", h1, padding=(spacing*2, 0, 0)),
            align_items,
            KeepTogether(
                flowables=[
                    FlexParagraph2("AlignContent", h1, padding=(spacing * 2, 0, 0)),
                    align_content,
                ]
            )
        ]
    )