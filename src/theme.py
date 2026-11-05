import tkinter as tk
from tkinter import ttk

BACKGROUND = "#0D0D0D"
SIDEBAR = "#252525"
PRIMARY = "#E10600"
SECONDARY = "#FFFFFF"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#AAAAAA"
BUTTON_HOVER = "#383838"

FONT_LOGO = ("Arial", 16, "bold")
FONT_HEADER = ("Arial", 24, "bold")
FONT_MENU = ("Arial", 11)


def setup_theme(root: tk.Tk):
    """Configura o estilo escuro (Dark Theme) para widgets do ttk (Treeview, Combobox, Scrollbar)."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # ==================== TREEVIEW (TABELA) ====================
    style.configure(
        "Treeview",
        background="#181818",
        foreground=TEXT_PRIMARY,
        fieldbackground="#181818",
        borderwidth=0,
        font=("Arial", 9),
        rowheight=26,
    )
    style.map(
        "Treeview",
        background=[("selected", "#2D2D2D")],
        foreground=[("selected", TEXT_PRIMARY)],
    )

    style.configure(
        "Treeview.Heading",
        background=SIDEBAR,
        foreground=TEXT_PRIMARY,
        font=("Arial", 9, "bold"),
        borderwidth=1,
        relief="flat",
    )
    style.map(
        "Treeview.Heading",
        background=[("active", BUTTON_HOVER)],
        foreground=[("active", TEXT_PRIMARY)],
    )

    # ==================== COMBOBOX (DROPDOWN) ====================
    style.configure(
        "TCombobox",
        background="#1E1E1E",
        foreground=TEXT_PRIMARY,
        fieldbackground="#1E1E1E",
        darkcolor="#1E1E1E",
        lightcolor="#333333",
        arrowcolor=TEXT_PRIMARY,
        bordercolor="#333333",
        selectbackground="#2D2D2D",
        selectforeground=TEXT_PRIMARY,
        insertcolor=TEXT_PRIMARY,
        padding=4,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", "#1E1E1E"), ("disabled", "#141414")],
        foreground=[("readonly", TEXT_PRIMARY), ("disabled", "#666666")],
        selectbackground=[("readonly", "#2D2D2D")],
        selectforeground=[("readonly", TEXT_PRIMARY)],
        background=[("active", BUTTON_HOVER)],
        arrowcolor=[("disabled", "#555555")],
    )

    # Garante que a lista suspensa (popdown/listbox) do Combobox também seja escura
    root.option_add("*TCombobox*Listbox.background", "#1E1E1E")
    root.option_add("*TCombobox*Listbox.foreground", TEXT_PRIMARY)
    root.option_add("*TCombobox*Listbox.selectBackground", "#2D2D2D")
    root.option_add("*TCombobox*Listbox.selectForeground", TEXT_PRIMARY)
    root.option_add("*TCombobox*Listbox.font", ("Arial", 9))

    # ==================== SCROLLBAR ====================
    style.configure(
        "Vertical.TScrollbar",
        background=SIDEBAR,
        troughcolor=BACKGROUND,
        arrowcolor=TEXT_PRIMARY,
        borderwidth=0,
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", BUTTON_HOVER)],
    )
