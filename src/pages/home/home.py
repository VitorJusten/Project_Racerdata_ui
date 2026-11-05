import tkinter as tk

from components.sidebar import Sidebar
from pages.dashboard.dashboard import DashboardPage
from pages.pilotos.pilotos import PilotosPage
from theme import BACKGROUND, TEXT_PRIMARY, FONT_HEADER


class Home(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)

        self.pages = {
            "dashboard": DashboardPage,
            "pilotos": PilotosPage,
        }
        self._create_layout()
        self.show_page("dashboard")

    def _create_layout(self):
        # Menu lateral fixo (Sidebar)
        self.sidebar = Sidebar(
            self,
            on_navigate=self.show_page
        )
        self.sidebar.pack(side="left", fill="y")

        # Área de conteúdo dinâmico
        self.content = tk.Frame(self, bg=BACKGROUND)
        self.content.pack(side="right", fill="both", expand=True)

    def show_page(self, page_name: str):
        # Limpa o conteúdo atual da área principal
        for widget in self.content.winfo_children():
            widget.destroy()

        page_class = self.pages.get(page_name)
        if page_class:
            page = page_class(self.content)
            page.pack(fill="both", expand=True)
        else:
            # Placeholder caso a página não exista
            placeholder = tk.Frame(self.content, bg=BACKGROUND)
            placeholder.pack(fill="both", expand=True, padx=35, pady=30)
            tk.Label(
                placeholder,
                text=page_name.capitalize(),
                bg=BACKGROUND,
                fg=TEXT_PRIMARY,
                font=FONT_HEADER,
            ).pack(anchor="nw")
