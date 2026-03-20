from node import Node

class Graph:
    def __init__(self):
        self.adj = {}


    def add_node(self, node: Node):
        self.adj[node] = []


    def add_connection_downwards(self, parent_node: Node, child_node: Node):
        self.adj[parent_node].append(child_node)


    def initalizeGraph(self, starting_num: int) -> Node:
        root_node = Node(0, 0, 0, 0, starting_num)
        self.adj[root_node] = []
        return root_node
    
    def buildGraphTree(self, node: Node):
        if node.number <= 10:
            return
        
        child2 = self.div2(node)
        if child2:
            self.buildGraphTree(child2)

        child3 = self.div3(node)
        if child3:
            self.buildGraphTree(child3)

    def div2(self, divisibleNode: Node) -> Node:

        if divisibleNode.number % 2 != 0:
            if divisibleNode.number % 3 != 0:
                divisibleNode.number += 1
            else:
                pass #divide by 3
                return
        
        new_node = Node(divisibleNode.pl1points, 
                        divisibleNode.pl2points,
                        divisibleNode.turn,
                        divisibleNode.bank,
                        divisibleNode.number//2)
        
        if new_node.number <= 10:
            pass #end the game
        
        if divisibleNode.turn == 0:
            new_node.turn = 1
            new_node.pl2points += 2
        else:
            new_node.turn = 0
            new_node.pl1points += 2

        if new_node.number % 10 == 0 or new_node.number % 10 == 5:
            new_node.bank += 1

        self.add_node(new_node)
        divisibleNode.div2child = new_node
        self.add_connection_downwards(divisibleNode, new_node)
        return new_node
    
    def div3(self, divisibleNode: Node) -> Node:

        if divisibleNode.number % 3 != 0:
            if divisibleNode.number % 2 != 0:
                divisibleNode.number += 1
            else:
                pass #divide by 2
                return
        
        new_node = Node(divisibleNode.pl1points, 
                        divisibleNode.pl2points,
                        divisibleNode.turn,
                        divisibleNode.bank,
                        divisibleNode.number//3)
        
        if new_node.number <= 10:
            pass #end the game
        
        if divisibleNode.turn == 0:
            new_node.turn = 1
            new_node.pl1points += 3
        else:
            new_node.turn = 0
            new_node.pl2points += 3

        if new_node.number % 10 == 0 or new_node.number % 10 == 5:
            new_node.bank += 1

        self.add_node(new_node)
        divisibleNode.div3child = new_node
        self.add_connection_downwards(divisibleNode, new_node)
        return new_node
        


        
    