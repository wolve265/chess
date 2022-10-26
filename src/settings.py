from dataclasses import dataclass
from pygame.color import Color

import utils


@dataclass(frozen=True)
class Settings:
    """
    Class used for storing game settings
    """

    # Names
    WINDOW_CAPTION: str = 'Chess'

    # Paths
    MAIN_DIR: str       = utils.dirname(utils.dirname(__file__))
    IMG_DIR: str        = utils.join(MAIN_DIR, 'img')
    PIECES_IMG_DIR: str = utils.join(IMG_DIR, 'pieces')

    # Params
    ROW_NUM: int = 8
    COL_NUM: int = 8
    FPS:     int = 30

    SQUARE_LEN: int = 80
    BOARD_LEN:  int = ROW_NUM * SQUARE_LEN
    BORDER_LEN: int = 25
    WINDOW_LEN: int = BOARD_LEN + 2*BORDER_LEN
    FONT_SIZE:  int = 30

    BOARD_SIZE:  tuple[int, int] = (BOARD_LEN, BOARD_LEN)
    SQUARE_SIZE: tuple[int, int] = (SQUARE_LEN, SQUARE_LEN)
    WINDOW_SIZE: tuple[int, int] = (WINDOW_LEN, WINDOW_LEN)

    # Colors
    BACKGROUND_COLOR   = Color(92, 104, 81)
    SQUARE_BLACK_COLOR = Color(125, 148, 93)
    SQUARE_WHITE_COLOR = Color(238, 238, 213)
    BLACK_COLOR        = Color(0, 0, 0)
    WHITE_COLOR        = Color(255, 255, 255)

    # Popups
    POPUP_FONT_SIZE:        int = 50
    POPUP_TEXT_MARGIN:      int = 25
    POPUP_SPACING:          int = 25
    POPUP_BORDER_RADIUS:    int = 10
