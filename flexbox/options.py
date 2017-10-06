from fortnum.fortnum import Fortnum


class FlexDirection(Fortnum):
    class Row(Fortnum):
        @staticmethod
        def width(items):
            return sum(item.width for item in items)

        @staticmethod
        def container_width(rows):
            return max(row.width for row in rows)

        @staticmethod
        def height(items):
            return max(item.height for item in items)

        @staticmethod
        def container_height(rows):
            return sum(row.height for row in rows)

    class Column(Fortnum):
        @staticmethod
        def width(items):
            return max(item.width for item in items)

        @staticmethod
        def container_width(rows):
            return sum(row.width for row in rows)

        @staticmethod
        def height(items):
            return sum(item.height for item in items)

        @staticmethod
        def container_height(rows):
            return max(row.height for row in rows)


class FlexStart(Fortnum):
    @staticmethod
    def point(item, length, key):
        return 0

    @staticmethod
    def points(items, length, key):
        point = 0
        for item in items:
            yield point
            point += key(item)


class FlexEnd(Fortnum):
    @staticmethod
    def point(item, length, key):
        total = length
        return total - key(item)

    @staticmethod
    def points(items, length, key):
        total_space = length - sum(key(item) for item in items)

        point = total_space
        for item in items:
            yield point
            point += key(item)


class FlexCenter(Fortnum):
    @staticmethod
    def point(item, length, key):
        total = length
        return (total - key(item)) / 2

    @staticmethod
    def points(items, length, key):
        total_space = length - sum(key(item) for item in items)

        point = total_space / 2
        for item in items:
            yield point
            point += key(item)


class SpaceAround(Fortnum):
    @staticmethod
    def points(items, length, key):
        total_space = length - sum(key(item) for item in items)
        space = total_space / (len(items) * 2)

        point = space
        for item in items:
            yield point
            point += space * 2 + key(item)


class SpaceEvenly(Fortnum):
    @staticmethod
    def points(items, length, key):
        total_space = length - sum(key(item) for item in items)
        space = total_space / (len(items) + 1)

        point = space
        for item in items:
            yield point
            point += key(item) + space


class SpaceBetween(Fortnum):
    @staticmethod
    def points(items, length, key):
        total_space = length - sum(key(item) for item in items)
        if len(items) == 1:
            yield total_space/2
        else:
            space = total_space / (len(items) - 1)

            point = 0
            for item in items:
                yield point
                point += key(item) + space


class Stretch(FlexStart):
    pass


class AlignItems(Fortnum):
    FlexStart = FlexStart
    FlexEnd = FlexEnd
    FlexCenter = FlexCenter


class AlignSelf(Fortnum):
    FlexStart = FlexStart
    FlexEnd = FlexEnd
    FlexCenter = FlexCenter


class JustifyContent(Fortnum):
    FlexStart = FlexStart
    FlexEnd = FlexEnd
    FlexCenter = FlexCenter
    SpaceAround = SpaceAround
    SpaceEvenly = SpaceEvenly
    SpaceBetween = SpaceBetween


class AlignContent(Fortnum):
    FlexStart = FlexStart
    FlexEnd = FlexEnd
    FlexCenter = FlexCenter
    SpaceAround = SpaceAround
    SpaceEvenly = SpaceEvenly
    SpaceBetween = SpaceBetween
    Stretch = Stretch


class FlexWrap(Fortnum):
    NoWrap = Fortnum("NoWrap")
    Wrap = Fortnum("Wrap")