from dataclasses import dataclass
from pygame.color import Color


@dataclass
class Settings:
    """
    Class used for storing game settings
    """

    # Names
    window_caption: str = 'Chess'

    # Params
    rows = cols = 8

    square_len: int = 80
    board_len:  int = rows * square_len
    border_len: int = 25
    window_len: int = board_len + 2*border_len
    font_size:  int = 30

    board_size:  tuple[int] = (board_len, board_len)
    square_size: tuple[int] = (square_len, square_len)
    window_size: tuple[int] = (window_len, window_len)

    #Colors
    background_color  = Color(92, 104, 81)
    black_color       = Color(125, 148, 93)
    white_color       = Color(238, 238, 213)
    black_piece_color = Color(0, 0, 0)
    white_piece_color = Color(255, 255, 255)
