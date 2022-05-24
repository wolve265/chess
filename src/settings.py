from dataclasses import dataclass


@dataclass
class Settings:
    """
    Class for storing game settings
    """

    window_caption: str = 'Chess'
    square_len: int = 80
    board_len: int = 8*square_len
