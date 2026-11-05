import threading
import tkinter as tk
from tkinter import messagebox
from typing import Optional
from datetime import datetime, date

from tkcalendar import DateEntry

from components.line_chart_component import LineChartComponent
from components.hierarchical_results_component import HierarchicalResultsComponent
from services.dashboard_service import DashboardService
from services.session_driver_service import SessionDriverService
from theme import BACKGROUND, SIDEBAR, PRIMARY, SECONDARY, TEXT_PRIMARY, TEXT_SECONDARY, BUTTON_HOVER, FONT_HEADER


class DashboardPage(tk.Frame):
    """
    Tela principal de Dashboard:
    - Barra superior com botão de coleta e seletores visuais de data (DateEntry)
    - Scroll geral na tela (Canvas + Scrollbar)
    - Gráfico de linha (LineChartComponent)
    - Hierarquia de resultados (HierarchicalResultsComponent)
    """

    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self._is_collecting = False
        self._filter_applied = False
        self._create_layout()
        self.load_data()

    def _create_layout(self):
        # Barra de Ações Superior (Fixa no topo)
        self.action_bar = tk.Frame(self, bg=SIDEBAR, highlightthickness=1, highlightbackground="#333333")
        self.action_bar.pack(fill="x", padx=15, pady=(10, 4))

        # Título da página
        tk.Label(
            self.action_bar,
            text="Dashboard de Performance",
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=12, pady=10)

        # Container dos controles à direita
        controls_frame = tk.Frame(self.action_bar, bg=SIDEBAR)
        controls_frame.pack(side="right", padx=12, pady=8)

        # Configuração visual do calendário dropdown (DateEntry)
        cal_kwargs = {
            "date_pattern": "yyyy-mm-dd",
            "background": "#1E1E1E",
            "foreground": TEXT_PRIMARY,
            "headersbackground": SIDEBAR,
            "headersforeground": TEXT_PRIMARY,
            "selectbackground": PRIMARY,
            "selectforeground": SECONDARY,
            "normalbackground": "#1E1E1E",
            "normalforeground": TEXT_PRIMARY,
            "weekendbackground": "#252525",
            "weekendforeground": TEXT_PRIMARY,
            "othermonthforeground": "#555555",
            "othermonthbackground": "#1E1E1E",
            "font": ("Arial", 9),
            "width": 11,
        }

        # Data Inicial (DateEntry)
        tk.Label(controls_frame, text="De:", bg=SIDEBAR, fg=TEXT_SECONDARY, font=("Arial", 9)).pack(side="left", padx=(0, 4))
        self.date_from_entry = DateEntry(
            controls_frame,
            year=datetime.now().year,
            month=1,
            day=1,
            **cal_kwargs
        )
        self.date_from_entry.pack(side="left", padx=(0, 10))

        # Data Final (DateEntry)
        tk.Label(controls_frame, text="Até:", bg=SIDEBAR, fg=TEXT_SECONDARY, font=("Arial", 9)).pack(side="left", padx=(0, 4))
        self.date_to_entry = DateEntry(
            controls_frame,
            year=datetime.now().year,
            month=12,
            day=31,
            **cal_kwargs
        )
        self.date_to_entry.pack(side="left", padx=(0, 8))

        # Checkbox ou botão para aplicar/limpar filtro de data
        self.var_use_date_filter = tk.BooleanVar(value=False)
        self.chk_use_filter = tk.Checkbutton(
            controls_frame,
            text="Filtrar por data",
            variable=self.var_use_date_filter,
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            selectcolor="#1E1E1E",
            activebackground=SIDEBAR,
            activeforeground=TEXT_PRIMARY,
            font=("Arial", 9),
            command=self.load_data
        )
        self.chk_use_filter.pack(side="left", padx=(0, 10))

        # Botão Aplicar Filtro
        self.btn_filter = tk.Button(
            controls_frame,
            text="Aplicar",
            bg="#383838",
            fg=TEXT_PRIMARY,
            activebackground="#4A4A4A",
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=10,
            command=self._on_apply_filter
        )
        self.btn_filter.pack(side="left", padx=(0, 14))

        # Botão Coletar Dados
        self.btn_collect = tk.Button(
            controls_frame,
            text="Coletar dados",
            bg=PRIMARY,
            fg=SECONDARY,
            activebackground="#B80500",
            activeforeground=SECONDARY,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=3,
            cursor="hand2",
            command=self._on_collect_clicked
        )
        self.btn_collect.pack(side="left")

        # Status / Feedback da coleta
        self.status_label = tk.Label(
            self,
            text="",
            bg=BACKGROUND,
            fg="#00ADB5",
            font=("Arial", 9, "italic")
        )
        self.status_label.pack(anchor="w", padx=18, pady=(0, 4))

        # =========================================================================
        # CONTAINER PRINCIPAL ROLÁVEL (Canvas + Scrollbar)
        # =========================================================================
        scroll_outer = tk.Frame(self, bg=BACKGROUND)
        scroll_outer.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.canvas = tk.Canvas(scroll_outer, bg=BACKGROUND, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(scroll_outer, orient="vertical", command=self.canvas.yview)

        self.main_content = tk.Frame(self.canvas, bg=BACKGROUND)
        self.main_content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_content, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Ajusta a largura do conteúdo interno automaticamente ao redimensionar a janela
        scroll_outer.bind("<Configure>", self._on_frame_resize)

        # Suporte a Scroll do Mouse (Wheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # 1. Gráfico de linha no topo
        self.line_chart = LineChartComponent(self.main_content)
        self.line_chart.pack(fill="x", pady=(0, 16))

        # 2. Hierarquia de resultados abaixo
        self.hierarchical_results = HierarchicalResultsComponent(self.main_content)
        self.hierarchical_results.pack(fill="x", expand=True)

    def _on_frame_resize(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width - 24)

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_apply_filter(self):
        self.var_use_date_filter.set(True)
        self.load_data()

    def load_data(self):
        """Carrega os dados dos dois endpoints aplicando o seletor de datas se ativado."""
        date_from = None
        date_to = None

        if self.var_use_date_filter.get():
            try:
                date_from_val: date = self.date_from_entry.get_date()
                date_to_val: date = self.date_to_entry.get_date()
                date_from = date_from_val.strftime("%Y-%m-%d")
                date_to = date_to_val.strftime("%Y-%m-%d")
            except Exception:
                date_from = None
                date_to = None

        try:
            # 1. Carrega dados do gráfico de linhas (apenas pilotos ativos no dashboard)
            chart_data = SessionDriverService.get_drivers_for_line_chart(
                date_from=date_from,
                date_to=date_to
            )
            self.line_chart.set_data(chart_data)

            # 2. Carrega hierarquia de resultados respeitando o intervalo de datas
            results_data = SessionDriverService.get_all_results(
                date_from=date_from,
                date_to=date_to
            )
            self.hierarchical_results.set_data(results_data)

        except Exception as e:
            messagebox.showerror(
                "Erro ao Carregar Dados",
                f"Não foi possível obter os dados do backend:\n{str(e)}"
            )

    def _on_collect_clicked(self):
        if self._is_collecting:
            return

        self._is_collecting = True
        self.btn_collect.config(state="disabled", text="Coletando...")
        self.status_label.config(text="Acessando a API OpenF1 e sincronizando sessões e pilotos...")

        thread = threading.Thread(target=self._run_collection, daemon=True)
        thread.start()

    def _run_collection(self):
        try:
            summary = DashboardService.collect_data()
            self.after(0, self._on_collection_success, summary)
        except Exception as e:
            self.after(0, self._on_collection_error, str(e))

    def _on_collection_success(self, summary):
        self._is_collecting = False
        self.btn_collect.config(state="normal", text="Coletar dados")
        self.status_label.config(text="Coleta concluída com sucesso!")

        info_msg = (
            f"Coleta concluída!\n\n"
            f"• Sessões encontradas: {summary.sessions_found}\n"
            f"• Novas sessões: {summary.sessions_new}\n"
            f"• Sessões atualizadas: {summary.sessions_updated}\n"
            f"• Pilotos identificados: {summary.drivers_found}\n"
            f"• Participações registradas: {summary.participations_created}\n"
            f"• Participações atualizadas: {summary.participations_updated}\n"
            f"• Erros: {summary.errors_count}"
        )
        messagebox.showinfo("Sucesso na Coleta", info_msg)

        # Recarrega os componentes após nova coleta
        self.load_data()

    def _on_collection_error(self, error_msg: str):
        self._is_collecting = False
        self.btn_collect.config(state="normal", text="Coletar dados")
        self.status_label.config(text="Falha durante a coleta de dados.")
        messagebox.showerror(
            "Erro na Coleta",
            f"Falha ao coletar dados da OpenF1:\n{error_msg}"
        )
