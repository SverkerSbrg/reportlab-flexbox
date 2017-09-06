.. _FlexItem:

========
FlexItem
========

A flowable providing a automatic wrapping function and basic css-style styling intended to be used as base-class for better flowables.

--------------------
Sizing your FlexItem
--------------------
Sizing flowables in ReportLab is build around the ``wrap(availWidth, availHeight)`` which allows each flowable to determine how much space they need given the avaliable width and height.

The size of a FlexItem is determined by two things

 - The min_width, width, max_width, min_height, height and max_height arguments
 - The size of its content, determined by the ``wrap_content(content_width, content_height)`` method used to determine the size of the content in the FlexItem. By default wrap_content returns 0, 0

The final size of the FlexItem is the largest of the two. That is if the content of a FlexItem is larger then the FlexItem's arguments stipulates the content size will take precedence.

-------
Styling
-------

Padding
'''''''

Margins
'''''''

Borders
'''''''

Background
''''''''''

--------------
Adding content
--------------

Two methods ´´wrap_content´´ and ´´draw_content´´


------------
FlexFlowable
------------
A simple utility class which empowers a existing Flowable by wrapping it in a FlexItem.

For example a ``FlexParagraph`` can be implemented like so:

.. literalinclude:: examples/flex_paragraph.py
    :lines: 6-11




