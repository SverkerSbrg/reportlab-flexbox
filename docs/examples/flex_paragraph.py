from reportlab.platypus import Paragraph

from flexbox import FlexFlowable


class FlexParagraph(FlexFlowable):
    def __init__(self, text, style):
        super().__init__(
            flowable=Paragraph(text, style),
            width="50%"
        )