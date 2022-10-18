from dataclasses import dataclass

import utils


@dataclass(frozen=True)
class Coord:
    row_i: int
    col_i: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.row_i + other.row_i, self.col_i + other.col_i)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(self.row_i - other.row_i, self.col_i - other.col_i)

    def __mul__(self, other: 'Coord') -> 'Coord':
        return Coord(self.row_i * other.row_i, self.col_i * other.col_i)

    def __floordiv__(self, other: 'Coord') -> 'Coord':
        row_i=other.row_i if other.row_i else 1
        col_i=other.col_i if other.col_i else 1
        return Coord(self.row_i // row_i, self.col_i // col_i)

    def __truediv__(self, other: 'Coord') -> 'Coord':
        return self.__floordiv__(other)

    def __lt__(self, other: 'Coord') -> bool:
        if self.row_i < other.row_i:
            return True
        if self.row_i > other.row_i:
            return False
        if self.col_i < other.col_i:
            return True
        return False

    def __gt__(self, other: 'Coord') -> bool:
        return not self.__lt__(other)

    def __abs__(self) -> 'Coord':
        return Coord(abs(self.row_i), abs(self.col_i))

    def __str__(self) -> str:
        row_str = self.get_row_str()
        col_str = self.get_col_str()
        return f"{col_str}{row_str}"

    def __repr__(self) -> str:
        row_str = self.get_row_str()
        col_str = self.get_col_str()
        return f"Coord({self.row_i}, {self.col_i}) = ({col_str}{row_str})"

    def get_row_str(self) -> str:
        return utils.row_int2str(self.row_i)

    def get_col_str(self) -> str:
        return utils.col_int2str(self.col_i)

    def get_direction(self) -> 'Coord':
        return self / abs(self)
