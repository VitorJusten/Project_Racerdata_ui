import tkinter as tk
from pages.home.home import Home
from theme import setup_theme, BACKGROUND


class Application(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("RacerData")
        self.geometry("1200x750")
        self.configure(bg=BACKGROUND)

        # Aplica estilização de tema escuro nos componentes ttk (Treeview, etc)
        setup_theme(self)

        self.home = Home(self)
        self.home.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
