import tkinter as tk

from theme import (
    SIDEBAR,
    PRIMARY,
    TEXT_PRIMARY,
    BUTTON_HOVER,
    FONT_LOGO,
    FONT_MENU
)


class Sidebar(tk.Frame):
    def __init__(self, parent, on_navigate):
        super().__init__(parent, bg=SIDEBAR, width=230)

        self.on_navigate = on_navigate
        self.pack_propagate(False)

        self._create_header()
        self._create_menu()

    def _create_header(self):
        header = tk.Frame(self, bg=SIDEBAR)
        header.pack(pady=(30, 40))

        tk.Label(
            header,
            text="RACER",
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            font=FONT_LOGO
        ).pack(side="left")

        tk.Label(
            header,
            text="DATA",
            bg=SIDEBAR,
            fg=PRIMARY,
            font=FONT_LOGO
        ).pack(side="left")

    def _create_menu(self):
        menu_items = [
            ("Dashboard", "dashboard"),
            ("Pilotos", "pilotos"),
        ]

        for label, page_name in menu_items:
            tk.Button(
                self,
                text=label,
                command=lambda name=page_name: self.on_navigate(name),
                bg=SIDEBAR,
                fg=TEXT_PRIMARY,
                activebackground=BUTTON_HOVER,
                activeforeground=TEXT_PRIMARY,
                font=FONT_MENU,
                relief="flat",
                bd=0,
                anchor="w",
                padx=25,
                pady=12,
                cursor="hand2"
            ).pack(fill="x")