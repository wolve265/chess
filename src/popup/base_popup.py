from dataclasses import dataclass, field
from typing import Any

import pygame as pg
from pygame.color import Color
from pygame.event import Event
from pygame.font import Font
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Group, Sprite
from pygame.surface import Surface

from settings import Settings

get_display_rect = pg.display.get_surface().get_rect


@dataclass
class PopupButtonData:
    fun: Any = lambda: None
    text: str = "Default Text"
    font_name: str | None = None
    font_size: int = Settings.POPUP_FONT_SIZE
    text_color: Color = Settings.BLACK_COLOR
    background_color: Color = Settings.BACKGROUND_COLOR
    text_margin: int = Settings.POPUP_TEXT_MARGIN
    center: tuple[int, int] = get_display_rect().center
    font: Font = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.font = Font(self.font_name, self.font_size)


class PopupButton(Sprite):
    def __init__(self, pbd: PopupButtonData = PopupButtonData(), *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.pbd = pbd
        self.fun = pbd.fun
        self.centerx = pbd.center[0]
        self.centery = pbd.center[1]
        self.image = self.pbd.font.render(self.pbd.text, True, self.pbd.text_color)
        self.rect = self.image.get_rect(center=self.center)
        self.big_rect = self.rect.inflate(self.pbd.text_margin, self.pbd.text_margin)

    @property
    def center(self) -> tuple[int, int]:
        return (self.centerx, self.centery)

    @center.setter
    def center(self, value: tuple[int, int]) -> None:
        self.centerx, self.centery = value

    def move(self, x: int, y: int) -> None:
        self.center = (self.centerx + x, self.centery + y)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image = self.pbd.font.render(self.pbd.text, True, self.pbd.text_color)
        self.rect = self.image.get_rect(center=self.center)
        self.big_rect = self.rect.inflate(self.pbd.text_margin, self.pbd.text_margin)
        return super().update(*args, **kwargs)

    def draw(self, surface: Surface) -> None:
        pg.draw.rect(
            surface,
            self.pbd.background_color,
            self.big_rect,
            border_radius=Settings.POPUP_BORDER_RADIUS,
        )


class PopupGroup(Group):
    def __init__(self, buttons: list[PopupButton]) -> None:
        self.buttons = buttons
        self.active = False
        self.setup()
        super().__init__(*self.buttons)

    def setup(self) -> None:
        self.update_first_button_center()
        self.update_buttons_spacing()

    def update_first_button_center(self) -> None:
        first_button = self.buttons[0]
        distance_to_margin = (
            (len(self.buttons) - 1) / 2 * (first_button.big_rect.height + Settings.POPUP_SPACING)
        )
        first_button.move(0, int(-distance_to_margin))

    def update_buttons_spacing(self) -> None:
        for i, button in enumerate(self.buttons, 1):
            if i == len(self.buttons):
                break
            button_nxt = self.buttons[i]
            button_nxt.center = button.center
            button_nxt.move(0, button.big_rect.height + Settings.POPUP_SPACING)

    def draw_fog(self, surface: Surface) -> None:
        fog_surface = Surface(get_display_rect().size)
        fog_surface.set_alpha(128)
        fog_surface.fill(Settings.BLACK_COLOR)
        surface.blit(fog_surface, get_display_rect().topleft)

    def draw_union_rect(self, surface: Surface) -> None:
        union_rect = Rect(*self.buttons[0].center, 0, 0)
        for rect in [button.big_rect for button in self.buttons]:
            union_rect.union_ip(rect)
        union_rect.inflate_ip(Settings.POPUP_TEXT_MARGIN, Settings.POPUP_TEXT_MARGIN)
        union_surface = Surface(union_rect.size)
        union_surface.set_alpha(100)
        union_surface.fill(Settings.SQUARE_WHITE_COLOR)
        surface.blit(union_surface, union_rect.topleft)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if not self.active:
            return
        return super().update(*args, **kwargs)

    def draw(self, surface: Surface) -> list[Rect]:
        if not self.active:
            return []
        self.draw_fog(surface)
        self.draw_union_rect(surface)
        for button in self.buttons:
            button.draw(surface)
        return super().draw(surface)

    def actions(self, event: Event) -> None:
        if not self.active:
            return
        if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
            for button in self.buttons:
                if button.big_rect.collidepoint(event.pos):
                    button.fun()
