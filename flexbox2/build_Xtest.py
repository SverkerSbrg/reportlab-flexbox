from datetime import datetime

from reportlab.lib.colors import HexColor

from flexbox2.flex import TestItem
from tests.dev_test import TestPage, TestDoc

doc = TestDoc(filename="test_%s.pdf" % datetime.now().strftime("%Y%m%d_%H%M%S"), pageTemplates=[TestPage()])

doc.build([TestItem(
    padding=10,
    border=10,
    margin=10,
    background_color=HexColor(0x999999),
    border_color=HexColor(0xFF0099),
    width="100%"
)])