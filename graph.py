# ============================================================
# graph.py — Estrutura de Dados #2: Grafo de Grid + BFS
#            + TSP Heurística do Vizinho Mais Próximo
# ============================================================

from collections import deque
import math


# ─────────────────────────────────────────────────────────────
# GRID GRAPH — cada tile é um nó; arestas = vizinhos ortogonais
# ─────────────────────────────────────────────────────────────

class GridGraph:
    """
    Grafo implícito sobre um grid 2D.
    Nós = tiles transitáveis.
    Arestas = conexões ortogonais (4-direcional).
    """

    def __init__(self, grid: list[list[int]], cols: int, rows: int):
        self.grid = grid
        self.cols = cols
        self.rows = rows

    def is_walkable(self, col: int, row: int, open_doors: set) -> bool:
        if col < 0 or row < 0 or col >= self.cols or row >= self.rows:
            return False
        tile = self.grid[row][col]
        if tile == 1:                          # parede
            return False
        if tile == 2:                          # porta
            return f"{col},{row}" in open_doors
        return True                            # chão, carpete, elevador

    def neighbors(self, col: int, row: int, open_doors: set) -> list:
        result = []
        for dc, dr in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nc, nr = col + dc, row + dr
            if self.is_walkable(nc, nr, open_doors):
                result.append((nc, nr))
        return result

    # ── BFS — caminho mínimo ──────────────────────────────────
    def find_path(self, sc: int, sr: int,
                  ec: int, er: int,
                  open_doors: set) -> list[tuple[int, int]]:
        """
        Busca em Largura (BFS).
        Retorna lista de (col, row) do próximo passo até o destino,
        ou [] se inalcançável.
        Complexidade: O(V + E) onde V = tiles, E = arestas.
        """
        if not self.is_walkable(ec, er, open_doors):
            return []
        if sc == ec and sr == er:
            return []

        encode = lambda c, r: r * self.cols + c
        visited = {encode(sc, sr)}
        parent: dict[int, int] = {}
        queue = deque([(sc, sr)])
        start_enc = encode(sc, sr)
        goal_enc  = encode(ec, er)

        while queue:
            c, r = queue.popleft()
            if c == ec and r == er:
                # Reconstrução do caminho
                path = []
                cur = goal_enc
                while cur != start_enc:
                    col_ = cur % self.cols
                    row_ = cur // self.cols
                    path.append((col_, row_))
                    cur = parent[cur]
                path.reverse()
                return path

            for nc, nr in self.neighbors(c, r, open_doors):
                nk = encode(nc, nr)
                if nk not in visited:
                    visited.add(nk)
                    parent[nk] = encode(c, r)
                    queue.append((nc, nr))

        return []   # destino inalcançável


# ─────────────────────────────────────────────────────────────
# TSP — Heurística do Vizinho Mais Próximo
# ─────────────────────────────────────────────────────────────

class TSPSolver:
    """
    Resolve o Problema do Caixeiro Viajante com a heurística
    do Vizinho Mais Próximo (Nearest Neighbor).
    Complexidade: O(n²)  — aceitável para n pequeno (2-5 NPCs).
    """

    @staticmethod
    def nearest_neighbor(start: tuple[int, int],
                         nodes: list[dict]) -> list[dict]:
        """
        Dado ponto de partida e lista de {id, col, row, name},
        retorna ordem de visita minimizando distância total.
        """
        if not nodes:
            return []

        visited: set[str] = set()
        route: list[dict] = []
        cur = start

        while len(visited) < len(nodes):
            best_dist = math.inf
            best_node = None
            for node in nodes:
                if node["id"] in visited:
                    continue
                d = math.hypot(node["col"] - cur[0], node["row"] - cur[1])
                if d < best_dist:
                    best_dist = d
                    best_node = node
            if best_node is None:
                break
            visited.add(best_node["id"])
            route.append(best_node)
            cur = (best_node["col"], best_node["row"])

        return route

    @staticmethod
    def route_distance(start: tuple[int, int],
                       route: list[dict]) -> float:
        total = 0.0
        prev = start
        for node in route:
            total += math.hypot(node["col"] - prev[0],
                                node["row"] - prev[1])
            prev = (node["col"], node["row"])
        return total
