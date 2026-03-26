import customtkinter as ctk


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class GameApp(ctk.CTk):
	def __init__(self) -> None:
		super().__init__()

		self.title("Division Game")
		self.geometry("1200x700")
		self.minsize(1000, 620)

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.current_frame = None
		self.show_start_screen()

	def show_screen(self, frame_cls, **kwargs) -> None:
		if self.current_frame is not None:
			self.current_frame.destroy()

		self.current_frame = frame_cls(self, **kwargs)
		self.current_frame.grid(row=0, column=0, sticky="nsew")

	def show_start_screen(self) -> None:
		self.show_screen(StartScreen)

	def show_mode_screen(self) -> None:
		self.show_screen(GameModeScreen)

	def show_game_screen(self, mode: str) -> None:
		self.show_screen(GameScreen, mode=mode)

	def show_game_over_screen(self, output_lines=None) -> None:
		if output_lines is None:
			output_lines = [
				"Player 1 wins",
				"Final score: 7 - 4",
				"Thanks for playing",
			]
		self.show_screen(GameOverScreen, output_lines=output_lines)


class StartScreen(ctk.CTkFrame):
	def __init__(self, master: GameApp) -> None:
		super().__init__(master)

		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure((0, 1, 2), weight=1)

		title = ctk.CTkLabel(self, text="Division Game", font=ctk.CTkFont(size=46, weight="bold"))
		title.grid(row=0, column=0, pady=(40, 10))

		start_btn = ctk.CTkButton(
			self,
			text="Start game",
			width=220,
			height=52,
			font=ctk.CTkFont(size=22, weight="bold"),
			command=master.show_mode_screen,
		)
		start_btn.grid(row=1, column=0, pady=10)


class GameModeScreen(ctk.CTkFrame):
	def __init__(self, master: GameApp) -> None:
		super().__init__(master)

		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure((0, 1, 2, 3), weight=1)

		title = ctk.CTkLabel(self, text="Choose game mode", font=ctk.CTkFont(size=38, weight="bold"))
		title.grid(row=0, column=0, pady=(35, 10))

		pvp_btn = ctk.CTkButton(
			self,
			text="Player vs player",
			width=300,
			height=56,
			font=ctk.CTkFont(size=24),
			command=lambda: master.show_game_screen("Player vs player"),
		)
		pvp_btn.grid(row=1, column=0, pady=8)

		pvc_btn = ctk.CTkButton(
			self,
			text="Player vs computer",
			width=300,
			height=56,
			font=ctk.CTkFont(size=24),
			command=lambda: master.show_game_screen("Player vs computer"),
		)
		pvc_btn.grid(row=2, column=0, pady=8)


class GameScreen(ctk.CTkFrame):
	def __init__(self, master: GameApp, mode: str) -> None:
		super().__init__(master)

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

		top_bar = ctk.CTkFrame(self, fg_color="transparent")
		top_bar.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 5))
		top_bar.grid_columnconfigure((0, 1, 2, 3), weight=1)

		ctk.CTkLabel(top_bar, text="P1 score: x", font=ctk.CTkFont(size=30)).grid(row=0, column=0, sticky="w")
		ctk.CTkLabel(top_bar, text="P2 score: x", font=ctk.CTkFont(size=30)).grid(row=0, column=1, sticky="w")
		ctk.CTkLabel(top_bar, text="Bank: x", font=ctk.CTkFont(size=30)).grid(row=0, column=2, sticky="w")
		ctk.CTkLabel(top_bar, text="Cur. NR: 5000", font=ctk.CTkFont(size=30)).grid(row=0, column=3, sticky="e")

		body = ctk.CTkFrame(self, fg_color="transparent")
		body.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 20))
		body.grid_rowconfigure(0, weight=1)
		body.grid_columnconfigure(0, weight=1)
		body.grid_columnconfigure(1, weight=0)
		body.grid_columnconfigure(2, weight=1)

		left_side = ctk.CTkFrame(body, fg_color="transparent")
		left_side.grid(row=0, column=0, sticky="nsew", padx=(10, 15), pady=10)
		left_side.grid_columnconfigure(0, weight=1)

		ctk.CTkLabel(left_side, text="Last turn:", font=ctk.CTkFont(size=46)).grid(row=0, column=0, pady=(20, 10))

		last_turn_values = ["15000", "/", "3", "=", "5000", "Player1 + 1 point", "Bank + 1 point"]
		for i, value in enumerate(last_turn_values, start=1):
			ctk.CTkLabel(left_side, text=value, font=ctk.CTkFont(size=42 if i < 6 else 36)).grid(
				row=i,
				column=0,
				pady=5,
			)

		divider = ctk.CTkFrame(body, width=5, corner_radius=0, fg_color="black")
		divider.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

		right_side = ctk.CTkFrame(body, fg_color="transparent")
		right_side.grid(row=0, column=2, sticky="n", padx=(15, 10), pady=40)
		right_side.grid_columnconfigure(0, weight=1)

		turn_label = "Player 1 turn" if mode == "Player vs computer" else "Player 2 turn"
		ctk.CTkLabel(right_side, text=turn_label, font=ctk.CTkFont(size=48)).grid(row=0, column=0, pady=(0, 20))

		btn_2 = ctk.CTkButton(
			right_side,
			text="/ 2",
			width=140,
			height=82,
			font=ctk.CTkFont(size=44),
			fg_color="transparent",
			border_width=3,
			border_color="black",
			text_color="black",
			hover_color="#d9d9d9",
		)
		btn_2.grid(row=1, column=0, pady=18)

		btn_3 = ctk.CTkButton(
			right_side,
			text="/ 3",
			width=140,
			height=82,
			font=ctk.CTkFont(size=44),
			fg_color="transparent",
			border_width=3,
			border_color="black",
			text_color="black",
			hover_color="#d9d9d9",
		)
		btn_3.grid(row=2, column=0, pady=18)

		game_over_btn = ctk.CTkButton(
			right_side,
			text="Game over",
			width=180,
			height=44,
			command=lambda: master.show_game_over_screen(
				[
					f"Mode: {mode}",
					"Bank total: 9",
					"Winner: Player 1",
				]
			),
		)
		game_over_btn.grid(row=3, column=0, pady=(40, 0))


class GameOverScreen(ctk.CTkFrame):
	def __init__(self, master: GameApp, output_lines: list[str]) -> None:
		super().__init__(master)

		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

		ctk.CTkLabel(self, text="Game over", font=ctk.CTkFont(size=52, weight="bold")).grid(
			row=0,
			column=0,
			pady=(35, 10),
		)

		lines_frame = ctk.CTkFrame(self, fg_color="transparent")
		lines_frame.grid(row=1, column=0, pady=(5, 10))

		for idx in range(3):
			line_text = output_lines[idx] if idx < len(output_lines) else ""
			ctk.CTkLabel(lines_frame, text=line_text, font=ctk.CTkFont(size=30)).grid(row=idx, column=0, pady=6)

		ctk.CTkButton(
			self,
			text="New game",
			width=220,
			height=52,
			font=ctk.CTkFont(size=22, weight="bold"),
			command=master.show_mode_screen,
		).grid(row=2, column=0, pady=20)


if __name__ == "__main__":
	app = GameApp()
	app.mainloop()