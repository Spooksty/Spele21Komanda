import customtkinter as ctk

_BTN_SELECTED = "#1565C0"
_BTN_DEFAULT = "#3a3a3a"
_NUM_SELECTED = "#1b5e20"
_NUM_DEFAULT = "#3a3a3a"
_ALG_SELECTED = "#6d28d9"
_ALG_DEFAULT = "#3a3a3a"


class ModeFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_mode: str | None = None
        self.selected_number: int | None = None
        self.selected_algorithm: str | None = None
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            self, text="← Atpakaļ", width=80,
            fg_color="transparent", hover_color="#333333",
            command=lambda: self.app.show_frame("StartFrame"),
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 0))

        ctk.CTkLabel(
            self, text="Game Setup",
            font=("Arial", 32, "bold"),
        ).grid(row=1, column=0, pady=(10, 30))

        # --- Mode ---
        ctk.CTkLabel(self, text="Izvēlies spēlēs pretinieku", font=("Arial", 15, "bold"),
                     text_color="#aaaaaa").grid(row=2, column=0, pady=(0, 8))

        mode_row = ctk.CTkFrame(self, fg_color="transparent")
        mode_row.grid(row=3, column=0)

        self.btn_pvp = ctk.CTkButton(
            mode_row, text="Player VS Player",
            width=180, height=46, font=("Arial", 14),
            fg_color=_BTN_DEFAULT,
            command=lambda: self._select_mode("pvp"),
        )
        self.btn_pvp.grid(row=0, column=0, padx=12)

        self.btn_pvai = ctk.CTkButton(
            mode_row, text="Player VS AI",
            width=180, height=46, font=("Arial", 14),
            fg_color=_BTN_DEFAULT,
            command=lambda: self._select_mode("pvai"),
        )
        self.btn_pvai.grid(row=0, column=1, padx=12)

        # --- Number ---
        ctk.CTkLabel(self, text="Izvēlies sākuma skaitli", font=("Arial", 15, "bold"),
                     text_color="#aaaaaa").grid(row=4, column=0, pady=(28, 8))

        self.num_row = ctk.CTkFrame(self, fg_color="transparent")
        self.num_row.grid(row=5, column=0)

        self.num_buttons: list[ctk.CTkButton] = []
        for i in range(5):
            btn = ctk.CTkButton(
                self.num_row, text="", width=130, height=46,
                font=("Arial", 14), fg_color=_NUM_DEFAULT,
            )
            btn.grid(row=0, column=i, padx=8)
            self.num_buttons.append(btn)

        # --- Algorithm (shown only in pvai mode) ---
        self.alg_label = ctk.CTkLabel(
            self, text="Izvēlies algoritmu", font=("Arial", 15, "bold"),
            text_color="#aaaaaa",
        )
        # not gridded yet — shown when pvai is selected

        self.alg_row = ctk.CTkFrame(self, fg_color="transparent")
        # not gridded yet

        self.btn_minimax = ctk.CTkButton(
            self.alg_row, text="Minimax",
            width=180, height=46, font=("Arial", 14),
            fg_color=_ALG_DEFAULT,
            command=lambda: self._select_algorithm("minimax"),
        )
        self.btn_minimax.grid(row=0, column=0, padx=12)

        self.btn_alphabeta = ctk.CTkButton(
            self.alg_row, text="Alpha-Beta",
            width=180, height=46, font=("Arial", 14),
            fg_color=_ALG_DEFAULT,
            command=lambda: self._select_algorithm("alphabeta"),
        )
        self.btn_alphabeta.grid(row=0, column=1, padx=12)

        # --- Start ---
        self.start_btn = ctk.CTkButton(
            self, text="Sākt spēli",
            width=200, height=50, font=("Arial", 16, "bold"),
            state="disabled",
            command=self._start_game,
        )
        self.start_btn.grid(row=8, column=0, pady=40)

    def on_show(self):
        # Reset selections
        self.selected_mode = None
        self.selected_number = None
        self.selected_algorithm = None
        self.btn_pvp.configure(fg_color=_BTN_DEFAULT)
        self.btn_pvai.configure(fg_color=_BTN_DEFAULT)
        self.btn_minimax.configure(fg_color=_ALG_DEFAULT)
        self.btn_alphabeta.configure(fg_color=_ALG_DEFAULT)
        self.alg_label.grid_remove()
        self.alg_row.grid_remove()
        self.start_btn.configure(state="disabled")
        # Refresh number buttons with latest generated numbers
        for i, btn in enumerate(self.num_buttons):
            n = self.app.game_state.numbers[i]
            btn.configure(
                text=str(n),
                fg_color=_NUM_DEFAULT,
                command=lambda num=n: self._select_number(num),
            )

    def _select_mode(self, mode: str):
        self.selected_mode = mode
        self.btn_pvp.configure(fg_color=_BTN_SELECTED if mode == "pvp" else _BTN_DEFAULT)
        self.btn_pvai.configure(fg_color=_BTN_SELECTED if mode == "pvai" else _BTN_DEFAULT)

        if mode == "pvai":
            self.alg_label.grid(row=6, column=0, pady=(28, 8))
            self.alg_row.grid(row=7, column=0)
        else:
            self.selected_algorithm = None
            self.btn_minimax.configure(fg_color=_ALG_DEFAULT)
            self.btn_alphabeta.configure(fg_color=_ALG_DEFAULT)
            self.alg_label.grid_remove()
            self.alg_row.grid_remove()

        self._update_start()

    def _select_number(self, number: int):
        self.selected_number = number
        for btn in self.num_buttons:
            is_selected = btn.cget("text") == str(number)
            btn.configure(fg_color=_NUM_SELECTED if is_selected else _NUM_DEFAULT)
        self._update_start()

    def _select_algorithm(self, algorithm: str):
        self.selected_algorithm = algorithm
        self.btn_minimax.configure(fg_color=_ALG_SELECTED if algorithm == "minimax" else _ALG_DEFAULT)
        self.btn_alphabeta.configure(fg_color=_ALG_SELECTED if algorithm == "alphabeta" else _ALG_DEFAULT)
        self._update_start()

    def _update_start(self):
        alg_ok = self.selected_mode == "pvp" or self.selected_algorithm is not None
        ready = self.selected_mode is not None and self.selected_number is not None and alg_ok
        self.start_btn.configure(state="normal" if ready else "disabled")

    def _start_game(self):
        algorithm = self.selected_algorithm or "minimax"
        self.app.game_state.start_game(self.selected_number, self.selected_mode, algorithm)
        self.app.close_tree_window()
        self.app.show_frame("GameFrame")
