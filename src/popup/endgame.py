from popup.base_popup import PopupButtonData, PopupButton, PopupGroup

from events import END_APP, gen_event


class EndGamePopupGroup(PopupGroup):
    buttons = [
        PopupButton(pbd=PopupButtonData(text="New Game")),
        PopupButton(pbd=PopupButtonData(text="Options")),
        PopupButton(pbd=PopupButtonData(text="Exit", fun=lambda: gen_event(END_APP))),
    ]

    def __init__(self) -> None:
        super().__init__(self.buttons)
