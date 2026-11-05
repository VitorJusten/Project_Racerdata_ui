import os
import tkinter as tk
from typing import List, Optional
import matplotlib
os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.environ.get("TEMP", "C:/Temp"), "matplotlib_cache"))
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from dto.session_driver_line_chart_dto import SessionDriverLineChartDto
from theme import BACKGROUND, SIDEBAR, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY


class LineChartComponent(tk.Frame):
    """
    Componente de gráfico de linhas para evolução de posições dos pilotos ativos
    com painel lateral de detalhes e descrições.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self._data: List[SessionDriverLineChartDto] = []
        self._create_layout()

    def _create_layout(self):
        # Container com duas colunas: Gráfico (esquerda) e Detalhes/Legenda (direita)
        self.chart_frame = tk.Frame(self, bg=BACKGROUND)
        self.chart_frame.pack(side="left", fill="both", expand=True)

        self.details_container = tk.Frame(self, bg=SIDEBAR, width=280)
        self.details_container.pack(side="right", fill="y", padx=(10, 0))
        self.details_container.pack_propagate(False)

        # Cabeçalho da legenda lateral
        tk.Label(
            self.details_container,
            text="Pilotos no Dashboard",
            bg=SIDEBAR,
            fg=TEXT_PRIMARY,
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=12, pady=(12, 6))

        # Canvas com scroll para detalhes dos pilotos
        self.details_canvas = tk.Canvas(self.details_container, bg=SIDEBAR, highlightthickness=0)
        self.details_scroll = tk.Scrollbar(self.details_container, orient="vertical", command=self.details_canvas.yview)
        self.details_list = tk.Frame(self.details_canvas, bg=SIDEBAR)

        self.details_list.bind(
            "<Configure>",
            lambda e: self.details_canvas.configure(scrollregion=self.details_canvas.bbox("all"))
        )
        self.details_window = self.details_canvas.create_window((0, 0), window=self.details_list, anchor="nw")
        self.details_canvas.configure(xscrollcommand=None, yscrollcommand=self.details_scroll.set)

        self.details_canvas.pack(side="left", fill="both", expand=True, padx=4)
        self.details_scroll.pack(side="right", fill="y")

        # Inicializa a figura do matplotlib
        self.fig = Figure(figsize=(7, 3.8), dpi=100, facecolor=BACKGROUND)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#161616")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self._render_empty_chart()

    def set_data(self, data: List[SessionDriverLineChartDto]):
        self._data = data
        self._render_chart()
        self._render_details()

    def _render_empty_chart(self, message: str = "Nenhum dado encontrado para o período."):
        self.ax.clear()
        self.ax.set_facecolor("#161616")
        self.ax.tick_params(colors=TEXT_SECONDARY)
        for spine in self.ax.spines.values():
            spine.set_color("#333333")
        self.ax.text(
            0.5, 0.5, message,
            color=TEXT_SECONDARY,
            ha="center", va="center",
            transform=self.ax.transAxes,
            fontsize=11
        )
        self.canvas.draw()

    def _render_chart(self):
        self.ax.clear()
        self.ax.set_facecolor("#161616")
        self.ax.grid(True, linestyle="--", alpha=0.25, color="#555555")
        self.ax.tick_params(colors=TEXT_SECONDARY, labelsize=8)
        for spine in self.ax.spines.values():
            spine.set_color("#333333")

        has_points = False
        all_positions = []

        for driver_series in self._data:
            if not driver_series.points_dto:
                continue

            x_vals = []
            y_vals = []

            for pt in driver_series.points_dto:
                if pt.x and pt.y is not None:
                    # Simplifica data para exibição no eixo X (ex: MM/DD)
                    date_label = str(pt.x)[:10]
                    x_vals.append(date_label)
                    y_vals.append(pt.y)
                    all_positions.append(pt.y)

            if x_vals and y_vals:
                has_points = True
                color = driver_series.tag_color or PRIMARY
                self.ax.plot(
                    x_vals,
                    y_vals,
                    marker="o",
                    markersize=5,
                    linewidth=2,
                    color=color,
                    label=driver_series.driver_name
                )

        if not has_points:
            self._render_empty_chart()
            return

        # Configurações do gráfico
        self.ax.set_title("Evolução de Posições nas Corridas", color=TEXT_PRIMARY, fontsize=12, pad=10)
        self.ax.set_ylabel("Posição", color=TEXT_SECONDARY, fontsize=9)

        # Inverte eixo Y pois a 1ª posição é o topo
        min_p = min(all_positions) if all_positions else 1
        max_p = max(all_positions) if all_positions else 20
        self.ax.set_ylim(max(max_p + 1, 10), max(min_p - 1, 0))
        self.ax.tick_params(axis="x", rotation=30)
        self.fig.tight_layout()
        self.canvas.draw()

    def _render_details(self):
        # Limpa itens anteriores
        for w in self.details_list.winfo_children():
            w.destroy()

        if not self._data:
            tk.Label(
                self.details_list,
                text="Nenhum piloto ativo.",
                bg=SIDEBAR,
                fg=TEXT_SECONDARY,
                font=("Arial", 9)
            ).pack(anchor="w", padx=8, pady=8)
            return

        for driver in self._data:
            card = tk.Frame(self.details_list, bg="#2D2D2D", highlightthickness=1, highlightbackground="#3D3D3D")
            card.pack(fill="x", padx=8, pady=4)

            # Barra superior do card com cor e nome
            header_bar = tk.Frame(card, bg="#2D2D2D")
            header_bar.pack(fill="x", padx=8, pady=(6, 2))

            color_tag = tk.Label(
                header_bar,
                text="   ",
                bg=driver.tag_color or PRIMARY,
                width=2
            )
            color_tag.pack(side="left", padx=(0, 6))

            tk.Label(
                header_bar,
                text=driver.driver_name,
                bg="#2D2D2D",
                fg=TEXT_PRIMARY,
                font=("Arial", 10, "bold")
            ).pack(side="left")

            # Descrição do piloto
            desc_text = driver.description if driver.description else "Sem descrição cadastrada."
            tk.Label(
                card,
                text=desc_text,
                bg="#2D2D2D",
                fg=TEXT_SECONDARY,
                font=("Arial", 8),
                justify="left",
                wraplength=220
            ).pack(anchor="w", padx=8, pady=(0, 6))
