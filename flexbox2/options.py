from fortnum.fortnum import Fortnum


class FlexDirection2(Fortnum):
    class Row2(Fortnum):
        pass

    class Column2(Fortnum):
        pass


class FlexStart2(Fortnum):
    @staticmethod
    def point(length, available):
        return 0

    @staticmethod
    def points(lengths, available):
        point = 0
        for length in lengths:
            yield point
            point += length


class FlexEnd2(Fortnum):
    @staticmethod
    def point(length, available):
        return available - length

    @staticmethod
    def points(lengths, available):
        point = available - sum(lengths)
        for length in lengths:
            yield point
            point += length


class FlexCenter2(Fortnum):
    @staticmethod
    def point(length, available):
        return (available - length)/2

    @staticmethod
    def points(lengths, available):
        point = (available - sum(lengths))/2
        for length in lengths:
            yield point
            point += length


class SpaceAround2(Fortnum):
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


class SpaceEvenly2(Fortnum):
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


class SpaceBetween2(Fortnum):
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


class Stretch2(FlexStart2):
    @staticmethod
    def stretch(lengths, available):
        space = max((available - sum(lengths))/len(lengths), 0)
        for length in lengths:
            yield length + space


class AlignItems2(Fortnum):
    FlexStart = FlexStart2
    FlexEnd = FlexEnd2
    FlexCenter = FlexCenter2


class AlignSelf2(Fortnum):
    FlexStart = FlexStart2
    FlexEnd = FlexEnd2
    FlexCenter = FlexCenter2


class JustifyContent2(Fortnum):
    FlexStart = FlexStart2
    FlexEnd = FlexEnd2
    FlexCenter = FlexCenter2
    SpaceAround = SpaceAround2
    SpaceEvenly = SpaceEvenly2
    SpaceBetween = SpaceBetween2


class AlignContent2(Fortnum):
    FlexStart = FlexStart2
    FlexEnd = FlexEnd2
    FlexCenter = FlexCenter2
    SpaceAround = SpaceAround2
    SpaceEvenly = SpaceEvenly2
    SpaceBetween2 = SpaceBetween2
    Stretch = Stretch2


class FlexWrap2(Fortnum):
    NoWrap2 = Fortnum("NoWrap2")
    Wrap2 = Fortnum("Wrap2")
