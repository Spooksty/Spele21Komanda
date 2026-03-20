class Node:
    def __init__(self, pl1points: int, pl2points: int, turn: int, bank: int, number: int):
        self.pl1points = pl1points
        self.pl2points = pl2points
        self.bank = bank
        self.turn = turn
        self.number = number
        self.div2child: Node = None
        self.div3child: Node = None


    

    