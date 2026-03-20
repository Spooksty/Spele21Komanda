import customtkinter as ctk


class GameOverFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        ctk.CTkLabel(self, text="Spēles beigas", font=("Arial", 46, "bold")).grid(
            row=0, column=0, pady=(60, 0))

        self.lbl_winner = ctk.CTkLabel(self, text="", font=("Arial", 24))
        self.lbl_winner.grid(row=1, column=0, pady=(10, 0))

        ctk.CTkFrame(self, height=2, fg_color="#444444", width=300).grid(
            row=2, column=0, pady=20)

        self.lbl_p1_score = ctk.CTkLabel(self, text="", font=("Arial", 16),
                                         text_color="#60a5fa")
        self.lbl_p1_score.grid(row=3, column=0, pady=4)

        self.lbl_p2_score = ctk.CTkLabel(self, text="", font=("Arial", 16),
                                         text_color="#f87171")
        self.lbl_p2_score.grid(row=4, column=0, pady=4)

        self.lbl_bank_score = ctk.CTkLabel(self, text="", font=("Arial", 16),
                                           text_color="#fbbf24")
        self.lbl_bank_score.grid(row=5, column=0, pady=(4, 30))

        ctk.CTkButton(
            self, text="Spēlēt vēlreiz",
            width=200, height=50, font=("Arial", 16, "bold"),
            command=self._play_again,
        ).grid(row=6, column=0, pady=(0, 60))

    def on_show(self):
        gs = self.app.game_state
        node = gs.current_node
        winner = gs.get_winner()

        if winner == "Tie":
            self.lbl_winner.configure(text="Neizšķirts!", text_color="#ffffff")
        else:
            color = "#60a5fa" if winner == "Player 1" else "#f87171"
            self.lbl_winner.configure(text=f"{winner} uzvar!", text_color=color)

        self.lbl_p1_score.configure(text=f"Player 1:  {node.pl1points} punkti")
        self.lbl_p2_score.configure(text=f"Player 2:  {node.pl2points} punkti")

    def _play_again(self):
        self.app.game_state.regenerate_numbers()
        self.app.close_tree_window()
        self.app.show_frame("ModeFrame")
