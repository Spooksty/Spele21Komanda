import customtkinter as ctk
import random
class Node:
    def __init__(self, p1points, p2points, banka, turn, number):
        self.p1 = p1points
        self.p2 = p2points
        self.banka = banka
        self.turn = turn
        self.number = number
        self.div2 = None
        self.div3 = None
        self.minmax = None
        self.ab = None

class gametree:
    def __init__(self):
        self.root = None

    def generate(self, value):
        new_node = Node(0,0,0,1,value)
        new_node.div2 = div2(new_node)
        new_node.div3 = div3(new_node)
        new_node.minmax = minmax(new_node)
        new_node.div2.ab = alphabetafun(new_node, new_node.div2)
        new_node.ab = new_node.div2.ab
        new_node.div3.ab = alphabetafun(new_node, new_node.div3)
        new_node.ab = min(new_node.div2.ab, new_node.div3.ab)
        self.root = new_node

    def measure(self, value):
        global minmax_calls, ab_calls

        node1 = Node(0,0,0,1,value)
        node1.div2 = div2(node1)
        node1.div3 = div3(node1)
        minmax_calls = 0
        minmax(node1)

        node2 = Node(0,0,0,1,value)
        node2.div2 = div2(node2)
        node2.div3 = div3(node2)
        ab_calls = 0
        minmax(node2)
        node2.div2.ab = alphabetafun(node2, node2.div2)
        node2.div3.ab = alphabetafun(node2, node2.div3)

def div2(oldnode):
    new_node = Node(oldnode.p1, oldnode.p2, oldnode.banka, oldnode.turn, oldnode.number / 2)
    if new_node.turn == 1:
        new_node.turn = 2
        new_node.p2 += 2
    else:
        new_node.turn = 1
        new_node.p1 += 2
    if new_node.number%5 == 0:
        new_node.banka += 1

    if new_node.number <= 10:
        if oldnode.turn == 1:
            new_node.p1 += new_node.banka
        else:
            new_node.p2 += new_node.banka
        new_node.banka = None
        return new_node
    
    if not new_node.number % 2 == 0 and not new_node.number % 3 == 0:
        if new_node.number % 5 == 0:
            new_node.banka -= 1
        new_node.number += 1
        if new_node.number % 5 == 0:
            new_node.banka += 1
    if new_node.number % 2 == 0:
        new_node.div2 = div2(new_node)
    if new_node.number % 3 == 0:
        new_node.div3 = div3(new_node)
    return new_node
    
def div3(oldnode):
    new_node = Node(oldnode.p1, oldnode.p2, oldnode.banka, oldnode.turn, oldnode.number / 3)
    if new_node.turn == 1:
        new_node.turn = 2
        new_node.p1 += 3
    else:
        new_node.turn = 1
        new_node.p2 += 3
    if new_node.number%5 == 0:
        new_node.banka += 1

    if new_node.number <= 10:
        if oldnode.turn == 1:
            new_node.p1 += new_node.banka
        else:
            new_node.p2 += new_node.banka
        new_node.banka = None
        return new_node
    
    if not new_node.number % 2 == 0 and not new_node.number % 3 == 0:
        if new_node.number % 5 == 0:
            new_node.banka -= 1
        new_node.number += 1
        if new_node.number % 5 == 0:
            new_node.banka += 1
    if new_node.number % 2 == 0:
        new_node.div2 = div2(new_node)
    if new_node.number % 3 == 0:
        new_node.div3 = div3(new_node)
    return new_node

def minmax(node):
    global minmax_calls
    minmax_calls += 1
    if not node.div2 == None:
        node.div2.minmax = minmax(node.div2)
    if not node.div3 == None:
        node.div3.minmax = minmax(node.div3)
    if node.banka == None:
        if node.p1 > node.p2:
            return -1
        elif node.p1 < node.p2:
            return 1
        else:
            return 0
    if node.turn == 1:
        if node.div2 == None:
            return node.div3.minmax
        elif node.div3 == None:
            return node.div2.minmax
        else:
            return min(node.div2.minmax, node.div3.minmax)
    else:
        if node.div2 == None:
            return node.div3.minmax
        elif node.div3 == None:
            return node.div2.minmax
        else:
            return max(node.div2.minmax, node.div3.minmax)

def alphabetafun(node, prevnode):
    global ab_calls
    ab_calls += 1
    if node.banka == None:
        if node.p1 > node.p2:
            return -1
        elif node.p1 < node.p2:
            return 1
        else:
            return 0
    if not node.div2 == None:
        node.div2.ab = alphabetafun(node.div2, node)
        node.ab = node.div2.ab
    else:
        node.div3.ab = alphabetafun(node.div3, node)
        return node.div3.ab
    if node.div3 == None:
        return node.div2.ab
    if node.turn == 1:
        node.div3.ab = alphabetafun(node.div3, node)
        return min(node.div2.ab, node.div3.ab)
    else:
        if prevnode.ab == None:
            node.div3.ab = alphabetafun(node.div3, node)
            node.ab = max(node.div2.ab, node.div3.ab)
            return node.ab
        elif node.ab < prevnode.ab:
            node.div3.ab = alphabetafun(node.div3, node)
            node.ab = max(node.div2.ab, node.div3.ab)
            return node.ab
        else:            return node.ab

tree = gametree()
currentnode = None


minmax_calls = 0
ab_calls = 0

def run_experiment():
    global minmax_calls, ab_calls
    test_numbers = [random.randrange(10002, 20001, 6) for _ in range(10)]
    
    print(f"{'Skaitlis':>10} | {'MinMax mezgli':>14} | {'AB mezgli':>10} | {'Atzaroti %':>11}")
    print("-" * 75)

    prune_total = 0
    
    for num in test_numbers:
        tree.measure(num)
        mm_n = minmax_calls
        ab_n = ab_calls
        pruned = (1 - ab_n / mm_n) * 100
        prune_total = prune_total + pruned
        print(f"{num:>10} | {mm_n:>14} | {ab_n:>10} | {pruned:>10.1f}%")
    
    print(f"Vidējais atzarojums: {prune_total/len(test_numbers):.1f} %", )
    

run_experiment()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


BG_COLOR = "#2a073f"
CARD_COLOR = "#2507BC"
ACCENT_COLOR = "#001b6c"
ACCENT_HOVER = "#0a622d"
OUTLINE_COLOR = "#334155"
TEXT_PRIMARY = "#fcfeff"
TEXT_MUTED = "#cbd5e1"


def make_button(master, text: str, command, width: int, height: int, font_size: int, bold: bool = False):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        width=width,
        height=height,
        corner_radius=14,
        border_width=1,
        border_color=OUTLINE_COLOR,
        fg_color=ACCENT_COLOR,
        hover_color=ACCENT_HOVER,
        text_color=TEXT_PRIMARY,
        font=ctk.CTkFont(size=font_size, weight="bold" if bold else "normal"),
    )


class GameApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Division Game")
        self.geometry("1200x700")
        self.minsize(1000, 620)
        self.configure(fg_color=BG_COLOR)

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

    def show_ai_algorithm_screen(self) -> None:
        self.show_screen(AIAlgorithmScreen)
            
    def choose_number(self, ai_algorithm: int = 0) -> None:
        numbers = [random.randrange(10002, 20001, 6) for _ in range(5)]
        self.show_screen(ChooseNumberScreen, numbers=numbers, ai_algorithm=ai_algorithm)

    def show_game_screen(self, number: int = 5000, ai_algorithm: int = 0) -> None:
        tree.generate(number)
        global currentnode
        currentnode = tree.root
        self.show_screen(GameScreen, currentnode=currentnode, ai_algorithm=ai_algorithm)

    def show_game_over_screen(self, currentnode=None, ai_algorithm: int = 0) -> None:
        self.show_screen(GameOverScreen, currentnode=currentnode, ai_algorithm=ai_algorithm)


class StartScreen(ctk.CTkFrame):
    def __init__(self, master: GameApp) -> None:
        super().__init__(master, fg_color=BG_COLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        title = ctk.CTkLabel(
            self,
            text="Division Game",
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=46, weight="bold"),
        )
        title.grid(row=0, column=0, pady=(40, 10))

        start_btn = make_button(self, "Start game", master.show_mode_screen, 220, 52, 22, bold=True)
        start_btn.grid(row=1, column=0, pady=10)


class GameModeScreen(ctk.CTkFrame):
    def __init__(self, master: GameApp) -> None:
        super().__init__(master, fg_color=BG_COLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Choose game mode",
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=38, weight="bold"),
        )
        title.grid(row=0, column=0, pady=(35, 12))

        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=1, column=0)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        pvp_btn = make_button(
            buttons_frame,
            "Player vs player",
            master.choose_number,
            300,
            56,
            24,
        )
        pvp_btn.grid(row=0, column=0, padx=(0, 8), pady=0)

        pvc_btn = make_button(
            buttons_frame,
            "Player vs computer",
            master.show_ai_algorithm_screen,
            300,
            56,
            24,
        )
        pvc_btn.grid(row=0, column=1, padx=(8, 0), pady=0)


class AIAlgorithmScreen(ctk.CTkFrame):
    def __init__(self, master: GameApp) -> None:
        super().__init__(master, fg_color=BG_COLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Choose AI algorithm",
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=38, weight="bold"),
        )
        title.grid(row=0, column=0, pady=(35, 12))

        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=1, column=0)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        minmax_btn = make_button(
            buttons_frame,
            "Min-Max",
            lambda: master.choose_number(ai_algorithm=1),
            300,
            56,
            24,
        )
        minmax_btn.grid(row=0, column=0, padx=(0, 8), pady=0)

        alphabeta_btn = make_button(
            buttons_frame,
            "Alpha-Beta",
            lambda: master.choose_number(ai_algorithm=2),
            300,
            56,
            24,
        )
        alphabeta_btn.grid(row=0, column=1, padx=(8, 0), pady=0)
            
class ChooseNumberScreen(ctk.CTkFrame):
    def __init__(self, master: GameApp, numbers: list[int], ai_algorithm: int = 0) -> None:
        super().__init__(master, fg_color=BG_COLOR)

        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        title = ctk.CTkLabel(
            self,
            text="Choose starting number",
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=38, weight="bold"),
        )
        title.grid(row=0, column=0, columnspan=5, pady=(35, 10))

        for i, number in enumerate(numbers[:5]):
            number_btn = make_button(
                self,
                str(number),
                lambda selected_number=number: master.show_game_screen(selected_number, ai_algorithm),
                300,
                56,
                24,
            )
            number_btn.grid(row=1, column=i, padx=10, pady=8)


class GameScreen(ctk.CTkFrame):
    def __init__(self, master: GameApp, currentnode, ai_algorithm: int = 0) -> None:
        super().__init__(master, fg_color=BG_COLOR)
        self.currentnode = currentnode
        self.ai_algorithm = ai_algorithm
        self.last_turn_values = ["-", "/", "-", "=", "-", "No move yet", ""]

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 5))
        top_bar.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.p1_label = ctk.CTkLabel(top_bar, text="", text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=30))
        self.p1_label.grid(row=0, column=0, sticky="w")
        self.p2_label = ctk.CTkLabel(top_bar, text="", text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=30))
        self.p2_label.grid(row=0, column=1, sticky="w")
        self.bank_label = ctk.CTkLabel(top_bar, text="", text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=30))
        self.bank_label.grid(row=0, column=2, sticky="w")
        self.cur_nr_label = ctk.CTkLabel(top_bar, text="", text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=30))
        self.cur_nr_label.grid(row=0, column=3, sticky="e")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 20))
        body.grid_rowconfigure(0, weight=1)
        panel_width = 440
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=0, minsize=panel_width)
        body.grid_columnconfigure(2, weight=0)
        body.grid_columnconfigure(3, weight=0, minsize=panel_width)
        body.grid_columnconfigure(4, weight=1)

        left_side = ctk.CTkFrame(body, width=panel_width, fg_color=CARD_COLOR, corner_radius=18)
        left_side.grid(row=0, column=1, sticky="ns", padx=(10, 15), pady=10)
        left_side.grid_propagate(False)
        left_side.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left_side, text="Last turn:", text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=46)).grid(row=0, column=0, pady=(20, 10))

        self.last_turn_labels = []
        for i, value in enumerate(self.last_turn_values, start=1):
            label = ctk.CTkLabel(
                left_side,
                text=value,
                text_color=TEXT_MUTED,
                font=ctk.CTkFont(size=42 if i < 6 else 36),
            )
            label.grid(row=i, column=0, pady=5)
            self.last_turn_labels.append(label)

        divider = ctk.CTkFrame(body, width=3, corner_radius=0, fg_color=OUTLINE_COLOR)
        divider.grid(row=0, column=2, sticky="ns", padx=10, pady=10)

        right_side = ctk.CTkFrame(body, width=panel_width, fg_color=CARD_COLOR, corner_radius=18)
        right_side.grid(row=0, column=3, sticky="ns", padx=(15, 10), pady=10)
        right_side.grid_propagate(False)
        right_side.grid_columnconfigure(0, weight=1, minsize=360)

        self.turn_label = ctk.CTkLabel(
            right_side,
            text="",
            width=360,
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=48),
        )
        self.turn_label.grid(row=0, column=0, pady=(25, 20), padx=30)

        self.btn_2 = ctk.CTkButton(
            right_side,
            text="/ 2",
            width=160,
            height=88,
            font=ctk.CTkFont(size=42, weight="bold"),
            corner_radius=16,
            border_width=2,
            border_color=OUTLINE_COLOR,
            fg_color="#1e293b",
            hover_color="#334155",
            text_color=TEXT_PRIMARY,
            command=self.choose_div2,
        )
        self.btn_2.grid(row=1, column=0, pady=18)

        self.btn_3 = ctk.CTkButton(
            right_side,
            text="/ 3",
            width=160,
            height=88,
            font=ctk.CTkFont(size=42, weight="bold"),
            corner_radius=16,
            border_width=2,
            border_color=OUTLINE_COLOR,
            fg_color="#1e293b",
            hover_color="#334155",
            text_color=TEXT_PRIMARY,
            command=self.choose_div3,
        )
        self.btn_3.grid(row=2, column=0, pady=18)

        self.refresh_screen()

    def format_number(self, value) -> str:
        if value is None:
            return "-"
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    def choose_div2(self) -> None:
        if self.ai_algorithm in (1, 2) and self.currentnode.turn == 2:
            return
        self.apply_move(2)

    def choose_div3(self) -> None:
        if self.ai_algorithm in (1, 2) and self.currentnode.turn == 2:
            return
        self.apply_move(3)

    def apply_move(self, divisor: int) -> None:
        next_node = self.currentnode.div2 if divisor == 2 else self.currentnode.div3
        if next_node is None:
            return

        prev_node = self.currentnode
        self.currentnode = next_node

        global currentnode
        currentnode = next_node

        self.last_turn_values = [
            self.format_number(prev_node.number),
            "/",
            str(divisor),
            "=",
            self.format_number(next_node.number),
            f"P1: {next_node.p1}  P2: {next_node.p2}",
            f"Bank: {self.format_number(next_node.banka)}",
        ]

        if next_node.number <= 10:
            self.master.show_game_over_screen(currentnode=next_node, ai_algorithm=self.ai_algorithm)
            return

        self.refresh_screen()

    def refresh_screen(self) -> None:
        node = self.currentnode
        self.p1_label.configure(text=f"P1 score: {node.p1}")
        if self.ai_algorithm in (1, 2):
            self.p2_label.configure(text=f"Computer score: {node.p2}")
        else:
            self.p2_label.configure(text=f"P2 score: {node.p2}")
        self.bank_label.configure(text=f"Bank: {self.format_number(node.banka)}")
        self.cur_nr_label.configure(text=f"Cur. NR: {self.format_number(node.number)}")
        if self.ai_algorithm in (1, 2) and node.turn == 2:
            self.turn_label.configure(text="Computer's turn")
        else:
            self.turn_label.configure(text=f"Player {node.turn} turn")

        for i, label in enumerate(self.last_turn_labels):
            label.configure(text=self.last_turn_values[i])

        is_computer_turn = self.ai_algorithm in (1, 2) and node.turn == 2
        self.btn_2.configure(state="normal" if (node.div2 is not None and not is_computer_turn) else "disabled")
        self.btn_3.configure(state="normal" if (node.div3 is not None and not is_computer_turn) else "disabled")

        if self.ai_algorithm == 1 and node.turn == 2 and node.number > 10:
            self.after(500, self.make_minmax_ai_move)
        elif self.ai_algorithm == 2 and node.turn == 2 and node.number > 10:
            self.after(500, self.make_alphabeta_ai_move)

    def make_minmax_ai_move(self) -> None:
        node = self.currentnode
        if node.div2 is None and node.div3 is None:
            return
        if node.div2 is None:
            self.apply_move(3)
            return
        if node.div3 is None:
            self.apply_move(2)
            return

        if node.div2.minmax > node.div3.minmax:
            self.apply_move(2)
        else:
            self.apply_move(3)

    def make_alphabeta_ai_move(self) -> None:
        node = self.currentnode
        if node.div2 is None and node.div3 is None:
            return
        if node.div2 is None:
            self.apply_move(3)
            return
        if node.div3 is None:
            self.apply_move(2)
            return

        if node.div2.ab > node.div3.ab:
            self.apply_move(2)
        else:
            self.apply_move(3)


class GameOverScreen(ctk.CTkFrame):
    def __init__(self, master: GameApp, currentnode=None, ai_algorithm: int = 0) -> None:
        super().__init__(master, fg_color=BG_COLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        ctk.CTkLabel(self, text="Game over", text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=52, weight="bold")).grid(
            row=0,
            column=0,
            pady=(35, 10),
        )

        lines_frame = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=18)
        lines_frame.grid(row=1, column=0, pady=(5, 10))

        if currentnode is None:
            output_lines = [
                "Player 1 wins",
                "Final score: 7 - 4",
                "Thanks for playing",
            ]
        else:
            winner = "Draw"
            if currentnode.p1 > currentnode.p2:
                winner = "Player 1 wins"
            elif currentnode.p2 > currentnode.p1:
                winner = "Computer wins" if ai_algorithm in (1, 2) else "Player 2 wins"

            output_lines = [
                winner,
                f"Final score: {currentnode.p1} - {currentnode.p2}",
                "Thanks for playing!",
            ]

        for idx in range(3):
            line_text = output_lines[idx] if idx < len(output_lines) else ""
            ctk.CTkLabel(lines_frame, text=line_text, text_color=TEXT_MUTED, font=ctk.CTkFont(size=30)).grid(row=idx, column=0, padx=30, pady=8)

        make_button(self, "New game", master.show_mode_screen, 220, 52, 22, bold=True).grid(row=2, column=0, pady=20)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()

