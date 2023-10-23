from events import END_APP, MAIN_MENU, gen_event
from popup.base_popup import PopupButton, PopupButtonData, PopupGroup


class EndGamePopupGroup(PopupGroup):
    buttons = [
        PopupButton(pbd=PopupButtonData(text="Main Menu", fun=lambda: gen_event(MAIN_MENU))),
        PopupButton(pbd=PopupButtonData(text="Options")),
        PopupButton(pbd=PopupButtonData(text="Exit", fun=lambda: gen_event(END_APP))),
    ]

    def __init__(self) -> None:
        super().__init__(self.buttons)
