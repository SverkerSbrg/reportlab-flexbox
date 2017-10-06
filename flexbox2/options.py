from fortnum.fortnum import Fortnum


class FlexDirection2(Fortnum):
    class Row2(Fortnum):
        main_dimension = lambda item: item.width
        second_dimension = lambda item: item.height

    class Column2(Fortnum):
        main_dimension = lambda item: item.height
        second_dimension = lambda item: item.width
