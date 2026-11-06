import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Callable

from dto.dashboard_driver_dto import DashboardDriverDto
from services.dashboard_driver_service import DashboardDriverService
from theme import BACKGROUND, SIDEBAR, PRIMARY, SECONDARY, TEXT_PRIMARY, TEXT_SECONDARY


class DriverListPage(tk.Frame):
    """
    Tabela com atributos de DashboardDriver do getAll:
    - ID, Nome do Piloto, Tag Color, Descrição, Ativo (Status)
    - Ações: Editar, Apagar e Ativar/Desativar
    - Botão para abrir o formulário de novo piloto
    """

    def __init__(
        self,
        parent,
        on_open_create: Callable[[], None],
        on_open_edit: Callable[[DashboardDriverDto], None]
    ):
        super().__init__(parent, bg=BACKGROUND)
        self.on_open_create = on_open_create
        self.on_open_edit = on_open_edit

        self._drivers: List[DashboardDriverDto] = []
        self._create_layout()
        self.load_drivers()

    def _create_layout(self):
        # Barra superior com título, campo de filtro e botão de novo piloto
        top_bar = tk.Frame(self, bg=SIDEBAR, highlightthickness=1, highlightbackground="#333333")
        top_bar.pack(fill="x", padx=15, pady=10)

        tk.Label(
            top_bar,
            text="Pilotos do Dashboard",
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=12, pady=10)

        # Controles à direita
        right_controls = tk.Frame(top_bar, bg=SIDEBAR)
        right_controls.pack(side="right", padx=12, pady=8)

        # Filtro de texto
        tk.Label(right_controls, text="Buscar:", bg=SIDEBAR, fg=TEXT_SECONDARY, font=("Arial", 9)).pack(side="left", padx=(0, 4))
        self.entry_filter = tk.Entry(right_controls, width=16, bg="#1E1E1E", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY)
        self.entry_filter.pack(side="left", padx=(0, 6))
        self.entry_filter.bind("<Return>", lambda e: self.load_drivers())

        btn_search = tk.Button(
            right_controls,
            text="Filtrar",
            bg="#383838",
            fg=TEXT_PRIMARY,
            activebackground="#4A4A4A",
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            font=("Arial", 9),
            padx=8,
            command=self.load_drivers
        )
        btn_search.pack(side="left", padx=(0, 14))

        # Botão Novo Piloto
        btn_new = tk.Button(
            right_controls,
            text="+ Novo Piloto",
            bg=PRIMARY,
            fg=SECONDARY,
            activebackground="#B80500",
            activeforeground=SECONDARY,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=3,
            cursor="hand2",
            command=self.on_open_create
        )
        btn_new.pack(side="left")

        # Container da Tabela
        table_container = tk.Frame(self, bg=BACKGROUND)
        table_container.pack(fill="both", expand=True, padx=15, pady=(0, 8))

        columns = ("name", "color", "status", "description")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("name", text="Piloto")
        self.tree.heading("color", text="Cor da Tag")
        self.tree.heading("status", text="Ativo no Dashboard")
        self.tree.heading("description", text="Descrição")

        self.tree.column("name", width=180, anchor="w")
        self.tree.column("color", width=110, anchor="center")
        self.tree.column("status", width=140, anchor="center")
        self.tree.column("description", width=340, anchor="w")

        scrollbar = tk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Barra de Ações (Editar, Ativar/Desativar, Apagar)
        action_bar = tk.Frame(self, bg=SIDEBAR, highlightthickness=1, highlightbackground="#333333")
        action_bar.pack(fill="x", padx=15, pady=(0, 10))

        tk.Label(
            action_bar,
            text="Ações para o piloto selecionado:",
            bg=SIDEBAR,
            fg=TEXT_SECONDARY,
            font=("Arial", 9, "italic")
        ).pack(side="left", padx=12, pady=8)

        btn_edit = tk.Button(
            action_bar,
            text="✏️ Editar",
            bg="#383838",
            fg=TEXT_PRIMARY,
            activebackground="#4A4A4A",
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=10,
            command=self._on_edit_clicked
        )
        btn_edit.pack(side="left", padx=4)

        btn_toggle = tk.Button(
            action_bar,
            text="🔄 Ativar / Desativar",
            bg="#2E4053",
            fg=TEXT_PRIMARY,
            activebackground="#34495E",
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=10,
            command=self._on_toggle_status_clicked
        )
        btn_toggle.pack(side="left", padx=4)

        btn_delete = tk.Button(
            action_bar,
            text="🗑️ Apagar",
            bg="#922B21",
            fg=TEXT_PRIMARY,
            activebackground="#A93226",
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=10,
            command=self._on_delete_clicked
        )
        btn_delete.pack(side="left", padx=4)

    def load_drivers(self):
        filter_text = self.entry_filter.get().strip() or None
        try:
            self._drivers = DashboardDriverService.get_all(filter_text=filter_text)
            self._render_rows()
        except Exception as e:
            messagebox.showerror("Erro ao carregar", f"Não foi possível obter os pilotos:\n{e.response.json().get("detail", str(e))}")

    def _render_rows(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for driver in self._drivers:
            status_text = "Sim" if driver.isActive else "Não"
            color_text = driver.tag_color or "#E10600"
            self.tree.insert(
                "",
                "end",
                iid=driver.id,
                values=(
                    driver.driver_name,
                    f"■ {color_text}",
                    status_text,
                    driver.description or "-"
                )
            )

    def _get_selected_driver(self) -> Optional[DashboardDriverDto]:
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Selecione um piloto na tabela para executar a ação.")
            return None
        selected_id = selected_items[0]
        return next((d for d in self._drivers if d.id == selected_id), None)

    def _on_edit_clicked(self):
        driver = self._get_selected_driver()
        if driver:
            self.on_open_edit(driver)

    def _on_toggle_status_clicked(self):
        driver = self._get_selected_driver()
        if not driver:
            return

        new_status = not driver.isActive
        action_word = "ativar" if new_status else "desativar"

        if not messagebox.askyesno("Confirmar Status", f"Deseja {action_word} o piloto '{driver.driver_name}' no dashboard?"):
            return

        try:
            DashboardDriverService.change_status(driver.id, new_status)
            self.load_drivers()
        except Exception as e:
            messagebox.showerror("Erro ao alterar status", f"Falha na requisição:\n{e.response.json().get("detail", str(e))}")

    def _on_delete_clicked(self):
        driver = self._get_selected_driver()
        if not driver:
            return

        if not messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja remover '{driver.driver_name}' do dashboard?\nEssa ação não pode ser desfeita."
        ):
            return

        try:
            DashboardDriverService.delete(driver.id)
            messagebox.showinfo("Sucesso", "Piloto removido do dashboard.")
            self.load_drivers()
        except Exception as e:
            messagebox.showerror("Erro ao apagar", f"Falha ao excluir piloto:\n{e.response.json().get("detail", str(e))}")
