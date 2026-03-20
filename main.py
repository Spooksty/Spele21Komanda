import customtkinter as ctk
from game_state import GameState
from frames.start_frame import StartFrame
from frames.mode_frame import ModeFrame
from frames.game_frame import GameFrame
from frames.gameover_frame import GameOverFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Number Game")
        self.geometry("1000x680")
        self.resizable(True, True)

        self.game_state = GameState()
        self.tree_window = None

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, ctk.CTkFrame] = {}
        for FrameClass in (StartFrame, ModeFrame, GameFrame, GameOverFrame):
            frame = FrameClass(container, self)
            self.frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    # ── Navigation ──────────────────────────────────────────────────────────

    def show_frame(self, name: str):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    # ── Tree window ─────────────────────────────────────────────────────────

    def open_tree_window(self):
        from tree_window import TreeWindow
        if self.tree_window and self.tree_window.winfo_exists():
            self.tree_window.focus()
        else:
            self.tree_window = TreeWindow(self, self.game_state)

    def close_tree_window(self):
        if self.tree_window and self.tree_window.winfo_exists():
            self.tree_window.destroy()
        self.tree_window = None

    def on_move_made(self):
        if self.tree_window and self.tree_window.winfo_exists():
            self.tree_window.redraw()


if __name__ == "__main__":
    app = App()
    app.mainloop()
