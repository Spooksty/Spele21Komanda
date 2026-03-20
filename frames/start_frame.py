import customtkinter as ctk


class StartFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(
            self, text="Skaitļu dalīšanas spēle",
            font=("Arial", 52, "bold"),
        ).grid(row=0, column=0, pady=(80, 10))

        ctk.CTkButton(
            self, text="Sākt spēli",
            width=220, height=56,
            font=("Arial", 20, "bold"),
            command=lambda: app.show_frame("ModeFrame"),
        ).grid(row=2, column=0)

