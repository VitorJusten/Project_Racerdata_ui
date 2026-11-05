import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional

from dto.session_driver_results_dto import (
    SessionDriverResultsDto,
    SessionResultDetailDto,
    DriverPositionResultDto,
)
from theme import BACKGROUND, SIDEBAR, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY


class HierarchicalResultsComponent(tk.Frame):
    """
    Componente hierárquico expansível:
    1º nível: Ano
    2º nível: Corrida / Sessão
    3º nível: Tabela de posições dos pilotos
    """

    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND)
        self._data: List[SessionDriverResultsDto] = []
        self._year_frames: Dict[int, tk.Frame] = {}
        self._expanded_years: Dict[int, bool] = {}
        self._expanded_sessions: Dict[str, bool] = {}
        self._create_layout()

    def _create_layout(self):
        # Título da seção
        title_bar = tk.Frame(self, bg=BACKGROUND)
        title_bar.pack(fill="x", pady=(10, 6))

        tk.Label(
            title_bar,
            text="Resultados das Sessões por Ano",
            bg=BACKGROUND,
            fg=TEXT_PRIMARY,
            font=("Arial", 14, "bold")
        ).pack(side="left")

        # Container rolável para acomodar a hierarquia
        self.canvas = tk.Canvas(self, bg=BACKGROUND, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content_frame = tk.Frame(self.canvas, bg=BACKGROUND)

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.bind("<Configure>", self._on_resize)
        self.canvas.configure(xscrollcommand=None, yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _on_resize(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width - 25)

    def set_data(self, data: List[SessionDriverResultsDto]):
        self._data = data
        self._render_tree()

    def _render_tree(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        if not self._data:
            tk.Label(
                self.content_frame,
                text="Nenhum resultado de sessão encontrado.",
                bg=BACKGROUND,
                fg=TEXT_SECONDARY,
                font=("Arial", 10)
            ).pack(anchor="w", padx=10, pady=10)
            return

        for year_result in self._data:
            year = year_result.year
            sessions = year_result.result_dto or []

            # 1º Nível: Card do Ano
            year_card = tk.Frame(self.content_frame, bg=SIDEBAR, highlightthickness=1, highlightbackground="#333333")
            year_card.pack(fill="x", padx=4, pady=4)

            # Barra do Ano clicável
            year_header = tk.Frame(year_card, bg=SIDEBAR, cursor="hand2")
            year_header.pack(fill="x", padx=10, pady=8)

            indicator_label = tk.Label(
                year_header,
                text="▶",
                bg=SIDEBAR,
                fg=PRIMARY,
                font=("Arial", 11, "bold")
            )
            indicator_label.pack(side="left", padx=(0, 8))

            tk.Label(
                year_header,
                text=f"Temporada {year}",
                bg=SIDEBAR,
                fg=TEXT_PRIMARY,
                font=("Arial", 12, "bold")
            ).pack(side="left")

            tk.Label(
                year_header,
                text=f"({len(sessions)} sessões)",
                bg=SIDEBAR,
                fg=TEXT_SECONDARY,
                font=("Arial", 10)
            ).pack(side="left", padx=(10, 0))

            # Container das sessões do ano (inicialmente oculto)
            sessions_container = tk.Frame(year_card, bg="#1E1E1E")

            def toggle_year(sc=sessions_container, ind=indicator_label, yr=year):
                is_open = self._expanded_years.get(yr, False)
                if is_open:
                    sc.pack_forget()
                    ind.config(text="▶")
                    self._expanded_years[yr] = False
                else:
                    sc.pack(fill="x", padx=12, pady=(0, 8))
                    ind.config(text="▼")
                    self._expanded_years[yr] = True

            year_header.bind("<Button-1>", lambda e, func=toggle_year: func())
            for child in year_header.winfo_children():
                child.bind("<Button-1>", lambda e, func=toggle_year: func())

            # 2º Nível: Sessões
            for session in sessions:
                sess_card = tk.Frame(sessions_container, bg="#262626", highlightthickness=1, highlightbackground="#3A3A3A")
                sess_card.pack(fill="x", padx=6, pady=3)

                sess_header = tk.Frame(sess_card, bg="#262626", cursor="hand2")
                sess_header.pack(fill="x", padx=8, pady=6)

                sess_ind = tk.Label(sess_header, text="▶", bg="#262626", fg="#00ADB5", font=("Arial", 10, "bold"))
                sess_ind.pack(side="left", padx=(0, 6))

                circuit_name = session.circuit_short_name or "Circuito"
                sess_type = session.session_type or "Sessão"
                sess_date = str(session.date_end)[:10] if session.date_end else ""

                tk.Label(
                    sess_header,
                    text=f"🏁 {circuit_name} ({sess_type})",
                    bg="#262626",
                    fg=TEXT_PRIMARY,
                    font=("Arial", 10, "bold")
                ).pack(side="left")

                tk.Label(
                    sess_header,
                    text=f"Data: {sess_date}",
                    bg="#262626",
                    fg=TEXT_SECONDARY,
                    font=("Arial", 9)
                ).pack(side="right")

                # 3º Nível: Tabela de Posições
                table_frame = tk.Frame(sess_card, bg="#1E1E1E")
                self._render_session_table(table_frame, session.drivers_positions_dto or [])

                def toggle_session(tf=table_frame, ind=sess_ind, s_id=session.session_id):
                    is_open = self._expanded_sessions.get(s_id, False)
                    if is_open:
                        tf.pack_forget()
                        ind.config(text="▶")
                        self._expanded_sessions[s_id] = False
                    else:
                        tf.pack(fill="x", padx=8, pady=(0, 6))
                        ind.config(text="▼")
                        self._expanded_sessions[s_id] = True

                sess_header.bind("<Button-1>", lambda e, func=toggle_session: func())
                for child in sess_header.winfo_children():
                    child.bind("<Button-1>", lambda e, func=toggle_session: func())

    def _render_session_table(self, parent: tk.Frame, drivers: List[DriverPositionResultDto]):
        if not drivers:
            tk.Label(
                parent,
                text="Nenhum piloto registrado para esta sessão.",
                bg="#1E1E1E",
                fg=TEXT_SECONDARY,
                font=("Arial", 9)
            ).pack(anchor="w", padx=6, pady=4)
            return

        columns = ("pos", "driver", "team", "number")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=min(len(drivers), 10))

        tree.heading("pos", text="Posição")
        tree.heading("driver", text="Piloto")
        tree.heading("team", text="Equipe")
        tree.heading("number", text="Nº Carro")

        tree.column("pos", width=70, anchor="center")
        tree.column("driver", width=200, anchor="w")
        tree.column("team", width=180, anchor="w")
        tree.column("number", width=70, anchor="center")

        # Ordena pilotos pela posição
        sorted_drivers = sorted(
            drivers,
            key=lambda d: d.driver_position if d.driver_position is not None else 999
        )

        for d in sorted_drivers:
            pos_label = str(d.driver_position) if d.driver_position is not None else "N/A"
            tree.insert(
                "",
                "end",
                values=(
                    pos_label,
                    d.driver_name,
                    d.team_name or "N/A",
                    d.car_number if d.car_number is not None else "N/A",
                )
            )

        tree.pack(fill="x", padx=4, pady=4)
