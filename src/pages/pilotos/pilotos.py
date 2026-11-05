import tkinter as tk
from typing import Optional

from dto.dashboard_driver_dto import DashboardDriverDto
from pages.pilotos.driver_list_page import DriverListPage
from pages.pilotos.driver_form_page import DriverFormPage
from theme import BACKGROUND


class PilotosPage(tk.Frame):
    """
    Página orquestradora do módulo de Pilotos:
    Alterna dinamicamente entre a Listagem (DriverListPage) e o Formulário (DriverFormPage).
    """

    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self._current_view: Optional[tk.Widget] = None
        self.show_list()

    def show_list(self):
        self._clear_view()
        self._current_view = DriverListPage(
            self,
            on_open_create=self.show_create_form,
            on_open_edit=self.show_edit_form
        )
        self._current_view.pack(fill="both", expand=True)

    def show_create_form(self):
        self._clear_view()
        self._current_view = DriverFormPage(
            self,
            on_save_success=self.show_list,
            on_cancel=self.show_list,
            edit_driver=None
        )
        self._current_view.pack(fill="both", expand=True)

    def show_edit_form(self, driver: DashboardDriverDto):
        self._clear_view()
        self._current_view = DriverFormPage(
            self,
            on_save_success=self.show_list,
            on_cancel=self.show_list,
            edit_driver=driver
        )
        self._current_view.pack(fill="both", expand=True)

    def _clear_view(self):
        if self._current_view:
            self._current_view.destroy()
            self._current_view = None
