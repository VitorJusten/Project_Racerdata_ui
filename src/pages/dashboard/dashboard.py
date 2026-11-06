import threading
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from datetime import datetime, date, timedelta

from tkcalendar import DateEntry

from components.line_chart_component import LineChartComponent
from components.hierarchical_results_component import HierarchicalResultsComponent
from services.dashboard_service import DashboardService
from services.session_driver_service import SessionDriverService
from theme import BACKGROUND, SIDEBAR, PRIMARY, SECONDARY, TEXT_PRIMARY, TEXT_SECONDARY, FONT_HEADER

class DashboardPage(tk.Frame):
    """
    Tela principal de Dashboard:
    - Barra superior com botao de coleta, seletores de data (DateEntry) e filtro de tipo de sessao
    - Scroll geral na tela (Canvas + Scrollbar)
    - Grafico de linha (LineChartComponent)
    - Hierarquia de resultados (HierarchicalResultsComponent)
    """

    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self._is_collecting = False
        self._create_layout()
        self.load_data()

    def _create_layout(self):
        # Barra de Acoes Superior (Fixa no topo)
        self.action_bar = tk.Frame(self, bg=SIDEBAR, highlightthickness=1, highlightbackground="#333333")
        self.action_bar.pack(fill="x", padx=15, pady=(10, 4))

        # Titulo da pagina
        tk.Label(
            self.action_bar,
            text="Dashboard de Performance",
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=12, pady=10)

        # Container dos controles a direita
        controls_frame = tk.Frame(self.action_bar, bg=SIDEBAR)
        controls_frame.pack(side="right", padx=12, pady=8)

        # Configuracao visual do calendario dropdown (DateEntry)
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

        # Datas default: de = 1 mes atras, ate = hoje
        today = date.today()
        one_month_ago = today - timedelta(days=30)

        # Data Inicial (DateEntry) - sempre habilitado
        tk.Label(controls_frame, text="De:", bg=SIDEBAR, fg=TEXT_SECONDARY, font=("Arial", 9)).pack(side="left", padx=(0, 4))
        self.date_from_entry = DateEntry(
            controls_frame,
            year=one_month_ago.year,
            month=one_month_ago.month,
            day=one_month_ago.day,
            **cal_kwargs
        )
        self.date_from_entry.pack(side="left", padx=(0, 10))

        # Data Final (DateEntry) - sempre habilitado
        tk.Label(controls_frame, text="Até:", bg=SIDEBAR, fg=TEXT_SECONDARY, font=("Arial", 9)).pack(side="left", padx=(0, 4))
        self.date_to_entry = DateEntry(
            controls_frame,
            year=today.year,
            month=today.month,
            day=today.day,
            **cal_kwargs
        )
        self.date_to_entry.pack(side="left", padx=(0, 14))

        # Botao Aplicar Filtro
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
            command=self.load_data
        )
        self.btn_filter.pack(side="left", padx=(0, 14))

        # Botao Coletar Dados
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
        # CONTAINER PRINCIPAL ROLAVEL (Canvas + Scrollbar)
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

        # Ajusta a largura do conteudo interno automaticamente ao redimensionar a janela
        scroll_outer.bind("<Configure>", self._on_frame_resize)

        # Suporte a Scroll do Mouse (Wheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # 1. Grafico de linha no topo
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

    def load_data(self):
        """Carrega os dados dos dois endpoints aplicando os filtros de data e tipo de sessao."""
        try:
            date_from_val: date = self.date_from_entry.get_date()
            date_to_val: date = self.date_to_entry.get_date()
            date_from = date_from_val.strftime("%Y-%m-%d")
            date_to = date_to_val.strftime("%Y-%m-%d")
        except Exception:
            date_from = None
            date_to = None

        try:
            # 1. Carrega dados do grafico de linhas (apenas pilotos ativos no dashboard)
            chart_data = SessionDriverService.get_drivers_for_line_chart(
                date_from=date_from,
                date_to=date_to,
                session_type=""
            )
            self.line_chart.set_data(chart_data)

            # 2. Carrega hierarquia de resultados respeitando o intervalo de datas e tipo de sessao
            results_data = SessionDriverService.get_all_results(
                date_from=date_from,
                date_to=date_to,
                session_type=""
            )
            self.hierarchical_results.set_data(results_data)

        except Exception as e:
            messagebox.showerror(
                "Erro ao Carregar Dados",
                str(e.response.json().get("detail", str(e)))
            )

    def _on_collect_clicked(self):
        if self._is_collecting:
            return

        self._is_collecting = True
        self.btn_collect.config(state="disabled", text="Coletando...")
        self.status_label.config(text="Acessando a API OpenF1 e sincronizando sessoes e pilotos...")

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
        self.status_label.config(text="Coleta concluida com sucesso!")

        info_msg = (
            f"Coleta concluida!\n\n"
            f"• Sessoes encontradas: {summary.sessions_found}\n"
            f"• Novas sessoes: {summary.sessions_new}\n"
            f"• Sessoes atualizadas: {summary.sessions_updated}\n"
            f"• Pilotos identificados: {summary.drivers_found}\n"
            f"• Participacoes registradas: {summary.participations_created}\n"
            f"• Participacoes atualizadas: {summary.participations_updated}\n"
            f"• Erros: {summary.errors_count}"
        )
        messagebox.showinfo("Sucesso na Coleta", info_msg)

        # Recarrega os componentes apos nova coleta
        self.load_data()

    def _on_collection_error(self, error_msg: str):
        self._is_collecting = False
        self.btn_collect.config(state="normal", text="Coletar dados")
        self.status_label.config(text="Falha durante a coleta de dados.")
        messagebox.showerror(
            "Erro na Coleta",
            f"Falha ao coletar dados da OpenF1:\n{error_msg}"
        )
