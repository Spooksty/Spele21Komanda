from node import Node


# ── Pre-computation ───────────────────────────────────────────────────────────

def precompute_scores(root: Node) -> dict:
    scores = {}
    _minimax(root, scores)
    return scores


def _minimax(node: Node, scores: dict) -> float:
    if node is None:
        return 0

    if node.div2child is None and node.div3child is None:
        value = node.pl1points - node.pl2points
        scores[id(node)] = value
        return value

    child_scores = []
    for child in [node.div2child, node.div3child]:
        if child is not None:
            child_scores.append(_minimax(child, scores))

    value = max(child_scores) if node.turn == 0 else min(child_scores)
    scores[id(node)] = value
    return value



def alphabeta(node: Node, alpha: float, beta: float) -> float:
    if node is None:
        return 0

    if node.div2child is None and node.div3child is None:
        return node.pl1points - node.pl2points

    if node.turn == 0:          
        value = float('-inf')
        for child in [node.div2child, node.div3child]:
            if child is None:
                continue
            value = max(value, alphabeta(child, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break           
        return value

    else:                       
        value = float('+inf')
        for child in [node.div2child, node.div3child]:
            if child is None:
                continue
            value = min(value, alphabeta(child, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break           
        return value


def get_ai_move(node: Node, scores: dict, algorithm: str = "minimax") -> int | None:

    children = []
    if node.div2child is not None:
        children.append((2, node.div2child))
    if node.div3child is not None:
        children.append((3, node.div3child))

    if not children:
        return None

    if algorithm == "alphabeta":
        scored = [(d, alphabeta(child, float('-inf'), float('+inf'))) for d, child in children]
    else:
        scored = [(d, scores.get(id(child), float('inf'))) for d, child in children]

    return min(scored, key=lambda x: x[1])[0]
