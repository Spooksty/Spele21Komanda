import customtkinter as ctk
from ai import get_ai_move


class GameFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Header ──────────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, height=58, corner_radius=0, fg_color="#1e1e2e")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure((0, 2, 4, 6, 8), weight=1)

        self.lbl_p1 = ctk.CTkLabel(header, text="Player 1: 0 p",
                                    font=("Arial", 14, "bold"), text_color="#60a5fa")
        self.lbl_p1.grid(row=0, column=0, padx=16, pady=16)

        ctk.CTkLabel(header, text="│", text_color="#444466").grid(row=0, column=1)

        self.lbl_bank = ctk.CTkLabel(header, text="Bank: 0",
                                     font=("Arial", 13), text_color="#fbbf24")
        self.lbl_bank.grid(row=0, column=2)

        ctk.CTkLabel(header, text="│", text_color="#444466").grid(row=0, column=3)

        self.lbl_current_header = ctk.CTkLabel(header, text="Pašreiz: —",
                                               font=("Arial", 14, "bold"))
        self.lbl_current_header.grid(row=0, column=4)

        ctk.CTkLabel(header, text="│", text_color="#444466").grid(row=0, column=5)

        self.lbl_p2 = ctk.CTkLabel(header, text="Player 2: 0 p",
                                    font=("Arial", 14, "bold"), text_color="#f87171")
        self.lbl_p2.grid(row=0, column=6, padx=16)

        ctk.CTkLabel(header, text="│", text_color="#444466").grid(row=0, column=7)

        ctk.CTkButton(
            header, text="Skatīt grafu", width=100, height=30,
            font=("Arial", 12), fg_color="#374151",
            command=self.app.open_tree_window,
        ).grid(row=0, column=8, padx=16)

        # ── Content (left + right panels) ───────────────────────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
        content.grid_columnconfigure((0, 1), weight=1)
        content.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(content, corner_radius=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        left.grid_columnconfigure(0, weight=1)
        self._build_left_panel(left)

        right = ctk.CTkFrame(content, corner_radius=10)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(3, weight=1)
        self._build_right_panel(right)

    def _build_left_panel(self, parent):
        ctk.CTkLabel(parent, text="Pēdējais gājiens",
                     font=("Arial", 17, "bold")).grid(row=0, column=0, pady=(22, 6))
        ctk.CTkFrame(parent, height=2, fg_color="#444444").grid(
            row=1, column=0, sticky="ew", padx=24, pady=(0, 16))

        self.lbl_lt_line1 = ctk.CTkLabel(parent, text="Nav vēl veiktu gājienu",
                                         font=("Arial", 14), text_color="#aaaaaa")
        self.lbl_lt_line1.grid(row=2, column=0, pady=4)

        self.lbl_lt_result = ctk.CTkLabel(parent, text="",
                                          font=("Arial", 22, "bold"))
        self.lbl_lt_result.grid(row=3, column=0, pady=(2, 12))

        self.lbl_lt_points = ctk.CTkLabel(parent, text="",
                                          font=("Arial", 13))
        self.lbl_lt_points.grid(row=4, column=0, pady=2)

        self.lbl_lt_bank = ctk.CTkLabel(parent, text="",
                                        font=("Arial", 13), text_color="#fbbf24")
        self.lbl_lt_bank.grid(row=5, column=0, pady=2)

    def _build_right_panel(self, parent):
        self.lbl_turn = ctk.CTkLabel(parent, text="—",
                                     font=("Arial", 18, "bold"))
        self.lbl_turn.grid(row=0, column=0, pady=(22, 6))

        ctk.CTkFrame(parent, height=2, fg_color="#444444").grid(
            row=1, column=0, sticky="ew", padx=24, pady=(0, 8))

        self.lbl_number = ctk.CTkLabel(parent, text="",
                                       font=("Arial", 54, "bold"))
        self.lbl_number.grid(row=2, column=0, pady=(10, 10))

        btn_row = ctk.CTkFrame(parent, fg_color="transparent")
        btn_row.grid(row=3, column=0, pady=(0, 30))

        self.btn_div2 = ctk.CTkButton(
            btn_row, text="÷ 2", width=130, height=54,
            font=("Arial", 22, "bold"),
            command=lambda: self._make_move(2),
        )
        self.btn_div2.grid(row=0, column=0, padx=16)

        self.btn_div3 = ctk.CTkButton(
            btn_row, text="÷ 3", width=130, height=54,
            font=("Arial", 22, "bold"),
            command=lambda: self._make_move(3),
        )
        self.btn_div3.grid(row=0, column=1, padx=16)

    # ── Public ──────────────────────────────────────────────────────────────

    def on_show(self):
        self.update_ui()

    def update_ui(self):
        gs = self.app.game_state
        node = gs.current_node

        # Header
        self.lbl_p1.configure(text=f"Player 1: {node.pl1points} pts")
        self.lbl_bank.configure(text=f"Bank: {node.bank}")
        self.lbl_current_header.configure(text=f"Current: {node.number}")
        self.lbl_p2.configure(text=f"Player 2: {node.pl2points} pts")

        # Right panel — current number
        self.lbl_number.configure(text=str(node.number))

        # Determine whose turn it is
        is_ai_turn = gs.mode == "pvai" and node.turn == 1
        turn_name = "Player 1" if node.turn == 0 else "Player 2"

        if is_ai_turn:
            self.lbl_turn.configure(text="AI rēķina...", text_color="#fbbf24")
            self.btn_div2.configure(state="disabled")
            self.btn_div3.configure(state="disabled")
            self.after(700, self._ai_move)
        else:
            color = "#60a5fa" if node.turn == 0 else "#f87171"
            self.lbl_turn.configure(text=f"{turn_name} gājiens", text_color=color)
            self.btn_div2.configure(
                state="normal" if node.div2child is not None else "disabled")
            self.btn_div3.configure(
                state="normal" if node.div3child is not None else "disabled")

        # Left panel — last turn info
        lt = gs.last_turn_info
        if lt is None:
            self.lbl_lt_line1.configure(text="No moves yet", text_color="#aaaaaa")
            self.lbl_lt_result.configure(text="")
            self.lbl_lt_points.configure(text="")
            self.lbl_lt_bank.configure(text="")
        else:
            self.lbl_lt_line1.configure(
                text=f"{lt.number_before}  ÷ {lt.divisor}",
                text_color="#ffffff")
            self.lbl_lt_result.configure(text=f"= {lt.number_after}")
            self.lbl_lt_points.configure(
                text=f"{lt.who_gained} gained {lt.points_gained} pts")
            self.lbl_lt_bank.configure(
                text="Bank +1" if lt.bank_gained else "Bank unchanged",
                text_color="#fbbf24" if lt.bank_gained else "#666666")

    # ── Private ─────────────────────────────────────────────────────────────

    def _make_move(self, divisor: int):
        gs = self.app.game_state
        if not gs.make_move(divisor):
            return
        self.app.on_move_made()
        if gs.is_game_over():
            self.app.show_frame("GameOverFrame")
        else:
            self.update_ui()

    def _ai_move(self):
        gs = self.app.game_state
        # Guard: game may have been reset before callback fired
        if gs.current_node is None or gs.is_game_over():
            return
        if gs.mode != "pvai" or gs.current_node.turn != 1:
            return
        divisor = get_ai_move(gs.current_node, gs.scores, gs.algorithm)
        if divisor is not None:
            self._make_move(divisor)
