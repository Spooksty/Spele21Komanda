from random import randint
from typing import List, Optional
from graph import Graph
from node import Node
from ai import precompute_scores


def generate_random_numbers() -> List[int]:
    seen = set()
    while len(seen) < 5:
        n = randint(10000, 20000)
        if n % 2 == 0 and n % 3 == 0:
            seen.add(n)
    return list(seen)


class LastTurnInfo:
    def __init__(self, number_before: int, divisor: int, number_after: int,
                 points_gained: int, who_gained: str, bank_gained: bool):
        self.number_before = number_before
        self.divisor = divisor
        self.number_after = number_after
        self.points_gained = points_gained
        self.who_gained = who_gained
        self.bank_gained = bank_gained


class GameState:
    def __init__(self):
        self.numbers: List[int] = generate_random_numbers()
        self.mode: Optional[str] = None         
        self.root: Optional[Node] = None
        self.current_node: Optional[Node] = None
        self.last_turn_info: Optional[LastTurnInfo] = None
        self.visited_node_ids: List[int] = []    
        self.scores: dict = {}                   
        self.algorithm: str = "minimax"

    def start_game(self, starting_number: int, mode: str, algorithm: str = "minimax"):
        self.mode = mode
        self.algorithm = algorithm
        g = Graph()
        self.root = g.initalizeGraph(starting_number)
        g.buildGraphTree(self.root)
        self.scores = precompute_scores(self.root) if algorithm == "minimax" else {}
        self.current_node = self.root
        self.last_turn_info = None
        self.visited_node_ids = [id(self.root)]

    def make_move(self, divisor: int) -> bool:
        prev = self.current_node
        next_node = prev.div2child if divisor == 2 else prev.div3child
        if next_node is None:
            return False


        turn = prev.turn 
        if divisor == 2:
            who_gained = "Player 2" if turn == 0 else "Player 1"
            points_gained = 2
        else:
            who_gained = "Player 1" if turn == 0 else "Player 2"
            points_gained = 3

        self.last_turn_info = LastTurnInfo(
            number_before=prev.number,
            divisor=divisor,
            number_after=next_node.number,
            points_gained=points_gained,
            who_gained=who_gained,
            bank_gained=next_node.bank > prev.bank,
        )
        self.current_node = next_node
        self.visited_node_ids.append(id(next_node))
        return True

    def is_game_over(self) -> bool:
        n = self.current_node
        return n is None or n.number <= 10 or (n.div2child is None and n.div3child is None)

    def get_winner(self) -> str:
        n = self.current_node
        if n.pl1points > n.pl2points:
            return "Player 1"
        if n.pl2points > n.pl1points:
            return "Player 2"
        return "Tie"

    def regenerate_numbers(self):
        self.numbers = generate_random_numbers()
