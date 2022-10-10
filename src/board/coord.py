from dataclasses import dataclass

import utils


@dataclass(unsafe_hash=True)
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
        return Coord(self.row_i // other.row_i, self.col_i // other.col_i)

    def __truediv__(self, other: 'Coord') -> 'Coord':
        return self.__floordiv__(other)

    def __eq__(self, other) -> bool:
        return True if self.row_i == other.row_i and self.col_i == other.col_i else False

    def __abs__(self) -> 'Coord':
        return Coord(abs(self.row_i), abs(self.col_i))

    def __str__(self) -> str:
        row_str = self.get_row_str()
        col_str = self.get_col_str()
        return f"{col_str}{row_str}"

    def __repr__(self) -> str:
        row_str = self.get_row_str()
        col_str = self.get_col_str()
        return f"Pos({self.row_i}, {self.col_i}) = ({col_str}{row_str})"

    def get_row_str(self) -> str:
        return utils.row_int2str(self.row_i)

    def get_col_str(self) -> str:
        return utils.col_int2str(self.col_i)

    def get_direction(self) -> 'Coord':
        abs_coord = abs(Coord(
            row_i=self.row_i if self.row_i else 1,
            col_i=self.col_i if self.col_i else 1
        ))
        return self / abs_coord
