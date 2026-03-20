import tkinter as tk
import customtkinter as ctk
from game_state import GameState

# ── Layout ──────────────────────────────────────────────────────────────────
NODE_W  = 68   
NODE_H  = 30   
CORNER  = 6     
H_GAP   = 80    
V_GAP   = 84   
MARGIN  = 60

# ── Palette ─────────────────────────────────────────────────────────────────
BG = "#0f172a"

# Current node
C_CUR_FILL    = "#1e3a8a"
C_CUR_GLOW    = "#3b82f6"   # outer glow ring
C_CUR_TEXT    = "#e0f2fe"

# Visited-path nodes
C_VIS_FILL    = "#14532d"
C_VIS_OUTLINE = "#4ade80"
C_VIS_TEXT    = "#dcfce7"

# Unvisited nodes
C_DEF_FILL    = "#1e293b"
C_DEF_OUTLINE = "#334155"
C_DEF_TEXT    = "#64748b"

# Edges
C_EDGE_VIS    = "#4ade80"   # bright green — visited path
C_EDGE_DEF    = "#1e3a5f"   # subtle — unvisited
W_EDGE_VIS    = 2
W_EDGE_DEF    = 1

# Labels on edges
C_LBL_VIS     = "#86efac"
C_LBL_DEF     = "#334155"


def _rounded_rect(canvas: tk.Canvas, x1, y1, x2, y2, r, **kw) -> int:
    """Draw a rounded rectangle using the polygon-smooth trick."""
    pts = [
        x1 + r, y1,    x2 - r, y1,   # top edge
        x2,     y1,    x2,     y1 + r,  # top-right corner
        x2,     y2 - r, x2,    y2,   # right edge → bottom-right
        x2 - r, y2,    x1 + r, y2,   # bottom edge
        x1,     y2,    x1,     y2 - r,  # bottom-left corner
        x1,     y1 + r, x1,    y1,   # left edge → top-left
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)


class TreeWindow(ctk.CTkToplevel):
    def __init__(self, parent, game_state: GameState):
        super().__init__(parent)
        self.game_state = game_state
        self.title("Spēles koks")
        self.geometry("1250x700")
        self._build_ui()
        self.redraw()

    # ── UI setup ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Legend bar
        legend = tk.Frame(self, bg="#1e293b", height=36)
        legend.pack(side="top", fill="x")

        for dot_color, label_text in [
            (C_CUR_GLOW,    "Pašreizējā virsotne"),
            (C_VIS_OUTLINE, "Veiktais ceļš"),
            (C_DEF_OUTLINE, "Neizskatīta virsotne"),
        ]:
            tk.Label(legend, text="⬟", fg=dot_color, bg="#1e293b",
                     font=("Arial", 13)).pack(side="left", padx=(16, 3))
            tk.Label(legend, text=label_text, fg="#94a3b8", bg="#1e293b",
                     font=("Arial", 10)).pack(side="left", padx=(0, 20))

        # Scrollable canvas
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(wrap, bg=BG, highlightthickness=0)
        h_bar = tk.Scrollbar(wrap, orient="horizontal", command=self.canvas.xview)
        v_bar = tk.Scrollbar(wrap, orient="vertical",   command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_bar.set, yscrollcommand=v_bar.set)

        h_bar.pack(side="bottom", fill="x")
        v_bar.pack(side="right",  fill="y")
        self.canvas.pack(fill="both", expand=True)

    # ── Public redraw (called on every game move) ────────────────────────────

    def redraw(self):
        self.canvas.delete("all")
        if self.game_state.root is None:
            return

        # Assign layout positions
        positions: dict[int, tuple[int, int]] = {}
        id_to_node: dict[int, object] = {}
        counter = [0]
        self._assign_positions(
            self.game_state.root, 0, counter, positions, id_to_node)

        if not positions:
            return

        # Convert (x_idx, depth) → pixel centre (cx, cy)
        pixel: dict[int, tuple[float, float]] = {
            nid: (MARGIN + x * H_GAP, MARGIN + d * V_GAP)
            for nid, (x, d) in positions.items()
        }

        max_x = max(p[0] for p in pixel.values()) + MARGIN + NODE_W
        max_y = max(p[1] for p in pixel.values()) + MARGIN + NODE_H
        self.canvas.configure(scrollregion=(0, 0, max_x, max_y))

        # Precompute visited-path sets
        visited_ids  = self.game_state.visited_node_ids
        visited_set  = set(visited_ids)
        visited_edges = {
            (visited_ids[i], visited_ids[i + 1])
            for i in range(len(visited_ids) - 1)
        }
        current_id = (id(self.game_state.current_node)
                      if self.game_state.current_node else None)

        # ① Unvisited edges (drawn first, underneath everything)
        self._draw_all_edges(
            self.game_state.root, pixel, visited_edges, visited_set, on_path=False)

        # ② Visited-path edges (drawn on top of unvisited ones)
        self._draw_all_edges(
            self.game_state.root, pixel, visited_edges, visited_set, on_path=True)

        # ③ Nodes
        for nid, node in id_to_node.items():
            if nid not in pixel:
                continue
            self._draw_node(nid, node, pixel[nid], visited_set, current_id)

    # ── Drawing helpers ──────────────────────────────────────────────────────

    def _draw_node(self, nid, node, centre, visited_set, current_id):
        cx, cy = centre
        x1 = cx - NODE_W / 2
        y1 = cy - NODE_H / 2
        x2 = cx + NODE_W / 2
        y2 = cy + NODE_H / 2

        if nid == current_id:
            # Outer glow ring
            _rounded_rect(self.canvas, x1 - 5, y1 - 5, x2 + 5, y2 + 5,
                          CORNER + 5, fill=C_CUR_GLOW, outline="")
            _rounded_rect(self.canvas, x1, y1, x2, y2,
                          CORNER, fill=C_CUR_FILL, outline=C_CUR_GLOW, width=2)
            text_color = C_CUR_TEXT

        elif nid in visited_set:
            _rounded_rect(self.canvas, x1, y1, x2, y2,
                          CORNER, fill=C_VIS_FILL, outline=C_VIS_OUTLINE, width=1)
            text_color = C_VIS_TEXT

        else:
            _rounded_rect(self.canvas, x1, y1, x2, y2,
                          CORNER, fill=C_DEF_FILL, outline=C_DEF_OUTLINE, width=1)
            text_color = C_DEF_TEXT

        self.canvas.create_text(cx, cy, text=str(node.number),
                                fill=text_color, font=("Arial", 9, "bold"))

    def _draw_all_edges(self, node, pixel, visited_edges, visited_set, on_path: bool):
        """
        Two-pass edge drawing:
          on_path=False → draw only unvisited edges
          on_path=True  → draw only visited-path edges
        This ensures path edges always render on top.
        """
        if node is None:
            return
        nid = id(node)
        if nid not in pixel:
            return
        px, py = pixel[nid]

        for child, label in [(node.div2child, "÷2"), (node.div3child, "÷3")]:
            if child is None:
                continue
            cid = id(child)
            if cid not in pixel:
                continue

            is_path_edge = (nid, cid) in visited_edges

            if is_path_edge != on_path:
                # Skip — not what this pass draws
                self._draw_all_edges(child, pixel, visited_edges, visited_set, on_path)
                continue

            cx, cy = pixel[cid]

            # S-curve edge (smooth bezier via 4-point spline)
            ey_start = py + NODE_H / 2
            ey_end   = cy - NODE_H / 2
            mid_y    = (ey_start + ey_end) / 2
            color    = C_EDGE_VIS if is_path_edge else C_EDGE_DEF
            width    = W_EDGE_VIS if is_path_edge else W_EDGE_DEF

            self.canvas.create_line(
                px,  ey_start,
                px,  mid_y,
                cx,  mid_y,
                cx,  ey_end,
                smooth=True, fill=color, width=width,
                capstyle=tk.ROUND, joinstyle=tk.ROUND,
            )

            # Edge label with opaque background
            lx = (px + cx) / 2
            ly = mid_y
            lbl_color = C_LBL_VIS if is_path_edge else C_LBL_DEF
            # Small background pill so label is readable over edges
            self.canvas.create_rectangle(
                lx - 9, ly - 7, lx + 9, ly + 7,
                fill=BG, outline="",
            )
            self.canvas.create_text(lx, ly, text=label,
                                    fill=lbl_color, font=("Arial", 8, "bold"))

            self._draw_all_edges(child, pixel, visited_edges, visited_set, on_path)

    # ── Layout ───────────────────────────────────────────────────────────────

    def _assign_positions(self, node, depth, counter, positions, id_to_node):
        """In-order traversal → natural left-to-right binary tree layout."""
        if node is None:
            return
        id_to_node[id(node)] = node
        self._assign_positions(
            node.div2child, depth + 1, counter, positions, id_to_node)
        positions[id(node)] = (counter[0], depth)
        counter[0] += 1
        self._assign_positions(
            node.div3child, depth + 1, counter, positions, id_to_node)
