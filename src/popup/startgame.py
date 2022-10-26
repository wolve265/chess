from popup.base_popup import PopupButtonData, PopupButton, PopupGroup

from events import END_APP, START_GAME, gen_event


class StartGamePopupGroup(PopupGroup):
    buttons = [
        PopupButton(pbd=PopupButtonData(text="Start Game", fun=lambda: gen_event(START_GAME))),
        PopupButton(pbd=PopupButtonData(text="Options")),
        PopupButton(pbd=PopupButtonData(text="Exit", fun=lambda: gen_event(END_APP))),
    ]

    def __init__(self) -> None:
        super().__init__(self.buttons)
