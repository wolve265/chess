from dataclasses import dataclass


@dataclass
class Settings:
    """
    Class for storing game settings
    """

    window_caption: str = 'Chess'
    rows = cols = 8
    square_len: int = 80
    board_len: int = rows * square_len
    border_len: int = 20
    window_len: int = board_len + border_len
    font_size: int = 20
    black_color: str = 'Black'
    white_color: str = 'Gray90'
