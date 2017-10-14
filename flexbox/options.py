from fortnum.fortnum import Fortnum


class FlexDirection(Fortnum):
    class Row(Fortnum):
        pass

    class Column(Fortnum):
        pass


class FlexStart(Fortnum):
    @staticmethod
    def point(length, available):
        return 0

    @staticmethod
    def points(lengths, available):
        point = 0
        for length in lengths:
            yield point
            point += length


class FlexEnd(Fortnum):
    @staticmethod
    def point(length, available):
        return available - length

    @staticmethod
    def points(lengths, available):
        point = available - sum(lengths)
        for length in lengths:
            yield point
            point += length


class FlexCenter(Fortnum):
    @staticmethod
    def point(length, available):
        return (available - length)/2

    @staticmethod
    def points(lengths, available):
        point = (available - sum(lengths))/2
        for length in lengths:
            yield point
            point += length


class SpaceAround(Fortnum):
    @staticmethod
    def points(lengths, available):
        total_space = (available - sum(lengths))
        if total_space < 0:
            space = 0
            point = total_space/2
        else:
            space = total_space / (len(lengths) * 2)
            point = space

        for length in lengths:
            yield point
            point += length + space * 2


class SpaceEvenly(Fortnum):
    @staticmethod
    def points(lengths, available):
        total_space = (available - sum(lengths))
        if total_space < 0:
            space = 0
            point = total_space/2
        else:
            space = total_space/(len(lengths) + 1)
            point = space

        for length in lengths:
            yield point
            point += length + space


class SpaceBetween(Fortnum):
    @staticmethod
    def points(lengths, available):
        if len(lengths) == 1:
            yield (available - sum(lengths))/2
        else:
            total_space = available - sum(lengths)
            if total_space < 0:
                space = 0
                point = total_space/2
            else:
                space = total_space / (len(lengths) - 1)
                point = 0

            for length in lengths:
                yield point
                point += length + space


class Stretch(FlexStart):
    @staticmethod
    def stretch(lengths, available):
        space = max((available - sum(lengths))/len(lengths), 0)
        for length in lengths:
            yield length + space


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
    SpaceBetween2 = SpaceBetween
    Stretch = Stretch


class FlexWrap(Fortnum):
    NoWrap = Fortnum("NoWrap")
    Wrap = Fortnum("Wrap")
