import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from typing import Optional, Callable, List, Dict

from dto.dashboard_driver_dto import DashboardDriverDto
from dto.dashboard_driver_input_dto import DashboardDriverInputDto
from dto.driver_dto import DriverDto
from services.dashboard_driver_service import DashboardDriverService
from services.driver_service import DriverService
from theme import BACKGROUND, SIDEBAR, PRIMARY, SECONDARY, TEXT_PRIMARY, TEXT_SECONDARY


class DriverFormPage(tk.Frame):
    """
    Formulário para Cadastro e Edição de DashboardDriver:
    - driver_id (Combobox de pilotos)
    - description (Texto descritivo)
    - tag_color (Seletor visual de cor)
    - isActive (Checkbox de ativação no dashboard)
    """

    def __init__(
        self,
        parent,
        on_save_success: Callable[[], None],
        on_cancel: Callable[[], None],
        edit_driver: Optional[DashboardDriverDto] = None
    ):
        super().__init__(parent, bg=BACKGROUND)
        self.on_save_success = on_save_success
        self.on_cancel = on_cancel
        self.edit_driver = edit_driver

        self._available_drivers: List[DriverDto] = []
        self._selected_color = edit_driver.tag_color if edit_driver else "#E10600"

        self._create_layout()
        self._load_available_drivers()

    def _create_layout(self):
        # Card centralizado
        container = tk.Frame(self, bg=BACKGROUND)
        container.pack(fill="both", expand=True, padx=40, pady=25)

        # Cabeçalho
        title_text = "Editar Piloto do Dashboard" if self.edit_driver else "Novo Piloto do Dashboard"
        tk.Label(
            container,
            text=title_text,
            bg=BACKGROUND,
            fg=TEXT_PRIMARY,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 20))

        # Card do Formulário
        form_card = tk.Frame(container, bg=SIDEBAR, highlightthickness=1, highlightbackground="#333333")
        form_card.pack(fill="x", pady=(0, 20), padx=2)

        content_inner = tk.Frame(form_card, bg=SIDEBAR)
        content_inner.pack(fill="x", padx=24, pady=20)

        # 1. Campo: Seleção de Piloto
        tk.Label(
            content_inner,
            text="Piloto *",
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 4))

        self.combo_driver = ttk.Combobox(content_inner, state="readonly", font=("Arial", 10))
        self.combo_driver.pack(fill="x", pady=(0, 16))

        # Se for edição, o piloto já vem selecionado e bloqueado para troca de driver_id
        if self.edit_driver:
            self.combo_driver.set(self.edit_driver.driver_name)
            self.combo_driver.config(state="disabled")

        # 2. Campo: Descrição
        tk.Label(
            content_inner,
            text="Descrição personalizada",
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 4))

        self.txt_description = tk.Text(
            content_inner,
            height=4,
            bg="#1E1E1E",
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            font=("Arial", 10),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#444444"
        )
        self.txt_description.pack(fill="x", pady=(0, 16))
        if self.edit_driver and self.edit_driver.description:
            self.txt_description.insert("1.0", self.edit_driver.description)

        # 3. Campo: Cor da Tag (Tag Color)
        tk.Label(
            content_inner,
            text="Cor da Tag no Gráfico",
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 4))

        color_row = tk.Frame(content_inner, bg=SIDEBAR)
        color_row.pack(fill="x", pady=(0, 16))

        self.lbl_color_preview = tk.Label(
            color_row,
            text="       ",
            bg=self._selected_color,
            relief="solid",
            borderwidth=1
        )
        self.lbl_color_preview.pack(side="left", padx=(0, 10))

        self.lbl_color_hex = tk.Label(
            color_row,
            text=self._selected_color,
            bg=SIDEBAR,
            fg=TEXT_SECONDARY,
            font=("Arial", 9)
        )
        self.lbl_color_hex.pack(side="left", padx=(0, 12))

        btn_pick_color = tk.Button(
            color_row,
            text="Escolher cor...",
            bg="#383838",
            fg=TEXT_PRIMARY,
            activebackground="#4A4A4A",
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            font=("Arial", 9),
            padx=10,
            command=self._on_pick_color
        )
        btn_pick_color.pack(side="left")

        # 4. Campo: Ativo (isActive)
        self.var_active = tk.BooleanVar(value=self.edit_driver.isActive if self.edit_driver else True)
        chk_active = tk.Checkbutton(
            content_inner,
            text="Ativo no Dashboard principal",
            variable=self.var_active,
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            selectcolor="#1E1E1E",
            activebackground=SIDEBAR,
            activeforeground=TEXT_PRIMARY,
            font=("Arial", 10)
        )
        chk_active.pack(anchor="w", pady=(0, 20))

        # Barra de Botões (Salvar / Cancelar)
        button_bar = tk.Frame(container, bg=BACKGROUND)
        button_bar.pack(fill="x")

        btn_save = tk.Button(
            button_bar,
            text="Salvar Alterações" if self.edit_driver else "Cadastrar Piloto",
            bg=PRIMARY,
            fg=SECONDARY,
            activebackground="#B80500",
            activeforeground=SECONDARY,
            relief="flat",
            font=("Arial", 10, "bold"),
            padx=16,
            pady=6,
            cursor="hand2",
            command=self._on_save
        )
        btn_save.pack(side="left", padx=(0, 10))

        btn_cancel = tk.Button(
            button_bar,
            text="Cancelar",
            bg="#383838",
            fg=TEXT_PRIMARY,
            activebackground="#4A4A4A",
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            font=("Arial", 10),
            padx=14,
            pady=6,
            command=self.on_cancel
        )
        btn_cancel.pack(side="left")

    def _load_available_drivers(self):
        try:
            self._available_drivers = DriverService.get_all()
            driver_names = [d.name for d in self._available_drivers]
            self.combo_driver["values"] = driver_names

            if not self.edit_driver and driver_names:
                self.combo_driver.current(0)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os pilotos:\n{e}")

    def _on_pick_color(self):
        color = colorchooser.askcolor(initialcolor=self._selected_color, title="Selecione a cor da Tag")
        if color and color[1]:
            self._selected_color = color[1]
            self.lbl_color_preview.config(bg=self._selected_color)
            self.lbl_color_hex.config(text=self._selected_color)

    def _on_save(self):
        description = self.txt_description.get("1.0", "end-1c").strip()
        is_active = self.var_active.get()

        if self.edit_driver:
            driver_id = self.edit_driver.driver_id
        else:
            selected_name = self.combo_driver.get().strip()
            if not selected_name:
                messagebox.showwarning("Aviso", "Selecione um piloto.")
                return

            matched = next((d for d in self._available_drivers if d.name == selected_name), None)
            if not matched:
                messagebox.showerror("Erro", "Piloto selecionado inválido.")
                return
            driver_id = matched.id

        input_dto = DashboardDriverInputDto(
            driver_id=driver_id,
            description=description,
            tag_color=self._selected_color,
            isActive=is_active
        )

        try:
            if self.edit_driver:
                DashboardDriverService.update(self.edit_driver.id, input_dto)
                messagebox.showinfo("Sucesso", "Piloto atualizado com sucesso!")
            else:
                DashboardDriverService.create(input_dto)
                messagebox.showinfo("Sucesso", "Piloto cadastrado no dashboard com sucesso!")

            self.on_save_success()
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar os dados:\n{e}")
