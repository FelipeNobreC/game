# ============================================================
# renderer.py — Renderizador pixel art com pygame
# ============================================================

import pygame
import math
from data import C, TILE, COLS, ROWS, ROOM_RANGES, DOOR_COLS, FLOORS

# ── Fontes (inicializadas em setup) ──────────────────────────
font_small  = None   # 8 px  — texto UI
font_medium = None   # 14 px — diálogo
font_large  = None   # 20 px — títulos

def init_fonts():
    global font_small, font_medium, font_large
    pygame.font.init()
    # Tenta carregar fonte pixel; fallback para monospace
    try:
        font_small  = pygame.font.SysFont("Courier New", 11, bold=True)
        font_medium = pygame.font.SysFont("Courier New", 15, bold=True)
        font_large  = pygame.font.SysFont("Courier New", 22, bold=True)
    except Exception:
        font_small  = pygame.font.Font(None, 14)
        font_medium = pygame.font.Font(None, 18)
        font_large  = pygame.font.Font(None, 26)

# ── Helpers ───────────────────────────────────────────────────

def blit_text(surf, text, x, y, font, color, shadow=True):
    if shadow:
        sh = font.render(text, False, (0, 0, 0))
        surf.blit(sh, (x+1, y+1))
    tx = font.render(text, False, color)
    surf.blit(tx, (x, y))
    return tx.get_width()

def blit_text_center(surf, text, cx, y, font, color, shadow=True):
    tx = font.render(text, False, color)
    x = cx - tx.get_width() // 2
    if shadow:
        sh = font.render(text, False, (0, 0, 0))
        surf.blit(sh, (x+1, y+1))
    surf.blit(tx, (x, y))

def draw_rect_border(surf, color, rect, border_color, bw=2):
    pygame.draw.rect(surf, color, rect)
    pygame.draw.rect(surf, border_color, rect, bw)

# ── Mapa ──────────────────────────────────────────────────────

def render_map(surf, grid, open_doors: set, elevator_on: bool, revealed_rooms: set = None):
    t = TILE
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * t, row * t
            tile = grid[row][col]

            if tile == 0:  # Chão do corredor
                pygame.draw.rect(surf, C["floor"], (x, y, t, t))
                # Grade sutil
                pygame.draw.rect(surf, C["floor_alt"], (x, y, t, 1))
                pygame.draw.rect(surf, C["floor_alt"], (x, y, 1, t))

            elif tile == 1:  # Parede
                pygame.draw.rect(surf, C["wall"], (x, y, t, t))
                pygame.draw.rect(surf, C["wall_top"], (x, y, t, 5))  # topo
                pygame.draw.rect(surf, C["wall_side"], (x, y+5, 3, t-5))  # lado esq
                # Tijolo
                boff = (row % 2) * (t // 2)
                pygame.draw.rect(surf, C["wall_side"],
                                 (x + boff % t, y + 6, t // 2, t - 6), 1)

            elif tile == 2:  # Porta
                key = f"{col},{row}"
                is_open = key in open_doors
                pygame.draw.rect(surf, C["door_frame"], (x, y, t, t))
                if is_open:
                    pygame.draw.rect(surf, C["door_open"], (x+3, y+2, t-6, t-2))
                    pygame.draw.rect(surf, C["bg"], (x+6, y+5, t-12, t-7))
                else:
                    pygame.draw.rect(surf, C["door"], (x+3, y+2, t-6, t-2))
                    # Maçaneta
                    pygame.draw.rect(surf, C["yellow"],
                                     (x + t//2 - 2, y + t//2, 5, 4))

            elif tile == 3:  # Elevador
                col_e = C["elev_on"] if elevator_on else C["elev_off"]
                bg_e  = (30, 55, 90) if elevator_on else (20, 30, 52)
                pygame.draw.rect(surf, bg_e, (x, y, t, t))
                pygame.draw.rect(surf, col_e, (x, y, t, t), 2)
                # Seta ▲
                pts_up = [(x + t//2, y+6), (x+8, y+18), (x+t-8, y+18)]
                pygame.draw.polygon(surf, col_e, pts_up)
                # Seta ▼
                pts_dn = [(x + t//2, y+t-6), (x+8, y+t-18), (x+t-8, y+t-18)]
                pygame.draw.polygon(surf, col_e, pts_dn)

            elif tile == 4:  # Carpete
                pygame.draw.rect(surf, C["carpet"], (x, y, t, t))
                pygame.draw.rect(surf, C["carpet_line"], (x+4, y+4, t-8, t-8), 1)
                pygame.draw.rect(surf, C["carpet_line"], (x+8, y+8, t-16, t-16), 1)

    # Névoa de guerra: cobre salas não reveladas (linhas 0-5)
    if revealed_rooms is not None:
        fog = pygame.Surface((t, t * 6), pygame.SRCALPHA)
        fog.fill((6, 8, 14, 252))
        for i, (cs, ce) in enumerate(ROOM_RANGES):
            if i not in revealed_rooms:
                for c in range(cs, ce + 1):
                    surf.blit(fog, (c * t, 0))
                # Marca "?" no centro da sala
                cx = (cs + ce) // 2 * t + t // 2
                cy = 3 * t
                mark = font_small.render("? ? ?", False, (40, 50, 70))
                surf.blit(mark, (cx - mark.get_width() // 2, cy - mark.get_height() // 2))


def render_room_labels(surf, rooms, revealed_rooms: set = None):
    t = TILE
    for i, (cs, ce) in enumerate(ROOM_RANGES):
        if revealed_rooms is not None and i not in revealed_rooms:
            continue
        cx = (cs + ce) // 2 * t + t // 2
        cy = 2 * t + 4
        name = rooms[i]["name"]
        blit_text_center(surf, name, cx, cy, font_small, (*C["hud_dim"], 200))


# ── Caminho BFS ────────────────────────────────────────────────

def render_path(surf, path):
    if not path:
        return
    for i, (c, r) in enumerate(path):
        alpha = int(80 + 120 * (i / max(len(path), 1)))
        s = pygame.Surface((8, 8), pygame.SRCALPHA)
        s.fill((*C["player"], alpha))
        surf.blit(s, (c * TILE + TILE//2 - 4, r * TILE + TILE//2 - 4))


# ── NPC ────────────────────────────────────────────────────────

def render_npc(surf, npc, defeated: bool, tick: int):
    t = TILE
    x = npc["tx"] * t
    y = npc["ty"] * t
    color = C["gray"] if defeated else npc["color"]
    hat   = C["gray"] if defeated else npc["hat_color"]

    # Hover suave
    hover = 0 if defeated else int(math.sin(tick * 0.06) * 2)

    # Sombra
    shadow_s = pygame.Surface((t - 8, 4), pygame.SRCALPHA)
    shadow_s.fill((0, 0, 0, 60))
    surf.blit(shadow_s, (x + 4, y + t - 4))

    # Pernas
    pygame.draw.rect(surf, C["npc_body"], (x + 9, y + 20 + hover, 5, 10))
    pygame.draw.rect(surf, C["npc_body"], (x + 17, y + 20 + hover, 5, 10))

    # Corpo (jaleco)
    body_col = (*color[:3],) if not defeated else C["gray"]
    pygame.draw.rect(surf, C["npc_body"], (x + 6, y + 10 + hover, t - 12, 12))
    pygame.draw.rect(surf, color, (x + 8, y + 11 + hover, t - 16, 10))

    # Cabeça
    pygame.draw.rect(surf, C["player_skin"], (x + 8, y + 3 + hover, t - 16, 10))

    # Olhos
    pygame.draw.rect(surf, C["dark"], (x + 10, y + 5 + hover, 3, 3))
    pygame.draw.rect(surf, C["dark"], (x + 19, y + 5 + hover, 3, 3))

    # Boca
    pygame.draw.rect(surf, C["dark"],
                     (x + 12, y + (12 if not defeated else 13) + hover, 8, 2))

    # Chapéu de formatura
    if not defeated:
        pygame.draw.rect(surf, hat, (x + 7, y + 1 + hover, t - 14, 4))
        pygame.draw.rect(surf, hat, (x + 4, y - 2 + hover, t - 8, 4))
        # Canudo
        pygame.draw.rect(surf, C["dark"], (x + t//2 - 1, y - 4 + hover, 2, 4))
        pygame.draw.rect(surf, C["yellow"], (x + t//2 - 3, y - 6 + hover, 6, 3))

    # Nome acima
    if not defeated:
        blit_text_center(surf, npc["name"],
                         x + t // 2, y - 16 + hover,
                         font_small, color)


# ── Livro no chão ──────────────────────────────────────────────

def render_book_drop(surf, drop, tick: int):
    if not drop["visible"]:
        return
    t = TILE
    x = drop["col"] * t
    y = drop["row"] * t
    bounce = int(math.sin(tick * 0.1) * 3)
    color = drop["color"]

    # Sombra
    shadow_s = pygame.Surface((t - 10, 4), pygame.SRCALPHA)
    shadow_s.fill((0, 0, 0, 80))
    surf.blit(shadow_s, (x + 5, y + t - 4))

    # Capa do livro
    pygame.draw.rect(surf, color, (x + 4, y + 5 + bounce, t - 8, t - 10))
    pygame.draw.rect(surf, C["book_spine"], (x + 4, y + 5 + bounce, 5, t - 10))

    # Linhas de texto
    for ly in [10, 14, 18]:
        pygame.draw.rect(surf, C["book_spine"],
                         (x + 12, y + ly + bounce, 12, 2))

    # Brilho
    glow = pygame.Surface((t, t), pygame.SRCALPHA)
    pygame.draw.rect(glow, (*color, 40), (2, 3 + bounce, t - 4, t - 6), 3)
    surf.blit(glow, (x, y))

    blit_text_center(surf, "LIVRO!", x + t // 2, y - 14 + bounce,
                     font_small, color)


# ── Jogador ────────────────────────────────────────────────────

def render_player(surf, player, tick: int):
    px = int(player["px"])
    py = int(player["py"])
    t = TILE

    moving = player["moving"]
    walk = int(math.sin(tick * 0.22) * 2) if moving else 0
    leg  = int(math.sin(tick * 0.22) * 4) if moving else 0

    # Sombra
    shadow_s = pygame.Surface((t - 8, 5), pygame.SRCALPHA)
    shadow_s.fill((0, 0, 0, 70))
    surf.blit(shadow_s, (px + 4, py + t - 5))

    # Pernas
    pygame.draw.rect(surf, (40, 60, 160),
                     (px + 8, py + 20 + walk, 5, 10 + leg))
    pygame.draw.rect(surf, (40, 60, 160),
                     (px + 17, py + 20 + walk, 5, 10 - leg))

    # Corpo
    pygame.draw.rect(surf, C["player_body"],
                     (px + 6, py + 10 + walk, t - 12, 12))
    pygame.draw.rect(surf, (30, 140, 190),
                     (px + 8, py + 11 + walk, t - 16, 10))

    # Braços
    pygame.draw.rect(surf, C["player_body"], (px + 2, py + 11 + walk, 5, 9))
    pygame.draw.rect(surf, C["player_body"],
                     (px + t - 7, py + 11 + walk, 5, 9))

    # Cabeça
    pygame.draw.rect(surf, C["player_skin"],
                     (px + 8, py + 2 + walk, t - 16, 10))

    # Olhos
    pygame.draw.rect(surf, C["dark"], (px + 10, py + 4 + walk, 3, 3))
    pygame.draw.rect(surf, C["dark"], (px + 19, py + 4 + walk, 3, 3))

    # Cabelo
    pygame.draw.rect(surf, C["player_hair"],
                     (px + 8, py + 2 + walk, t - 16, 3))

    # Mochila
    pygame.draw.rect(surf, C["player"], (px + t - 9, py + 10 + walk, 8, 11))
    pygame.draw.rect(surf, (40, 200, 150), (px + t - 8, py + 11 + walk, 6, 9))
    pygame.draw.rect(surf, (30, 160, 120), (px + t - 8, py + 11 + walk, 6, 4))


# ── Indicador de clique ───────────────────────────────────────

def render_click_indicator(surf, indicator):
    if indicator is None:
        return
    c, r, t_val, max_t = indicator
    progress = t_val / max_t
    alpha = int(255 * (1 - progress))
    radius = int(TILE // 2 * (0.5 + 0.5 * progress))
    cx = c * TILE + TILE // 2
    cy = r * TILE + TILE // 2
    ring = pygame.Surface((TILE * 2, TILE * 2), pygame.SRCALPHA)
    pygame.draw.circle(ring, (*C["player"], alpha),
                       (TILE, TILE), radius, 2)
    pygame.draw.circle(ring, (*C["player"], alpha // 2),
                       (TILE, TILE), int(radius * 1.5), 1)
    surf.blit(ring, (cx - TILE, cy - TILE))


# ── HUD Lateral ───────────────────────────────────────────────

HUD_X = COLS * TILE + 10
HUD_W = 220

def render_hud(surf, state, tsp_route, inventory):
    sx = HUD_X
    sw = HUD_W
    sh = ROWS * TILE
    t  = TILE

    # Fundo do HUD
    pygame.draw.rect(surf, C["hud_bg"], (sx, 0, sw, sh))
    pygame.draw.rect(surf, C["hud_border"], (sx, 0, sw, sh), 2)
    pygame.draw.line(surf, C["hud_border"], (sx, 0), (sx, sh), 2)

    y = 8

    def section(title):
        nonlocal y
        pygame.draw.rect(surf, (20, 30, 48), (sx + 4, y, sw - 8, 18))
        pygame.draw.rect(surf, C["hud_border"], (sx + 4, y, sw - 8, 18), 1)
        blit_text(surf, title, sx + 8, y + 3, font_small, C["hud_text"], shadow=False)
        y += 22

    def line(text, color=None, indent=4):
        nonlocal y
        c = color or C["white"]
        blit_text(surf, text, sx + indent + 4, y, font_small, c, shadow=True)
        y += 16

    # ── Andar ────────────────────────────────────
    section("[ ANDAR ]")
    floor_name = state["floor_name"]
    # quebra em 2 linhas se longo
    words = floor_name.split("—")
    if len(words) == 2:
        line(words[0].strip(), C["yellow"])
        line(words[1].strip(), C["hud_text"])
    else:
        line(floor_name, C["yellow"])
    y += 4

    # ── TSP Rota ──────────────────────────────────
    section("[ ROTA TSP ]")
    if not tsp_route:
        line("Sem professores", C["gray"])
    else:
        for i, node in enumerate(tsp_route):
            done = node["id"] in state["defeated"]
            cur  = (i == state.get("tsp_ptr", 0)) and not done
            if done:
                col = C["hud_dim"]
                prefix = "✓"
            elif cur:
                col = C["yellow"]
                prefix = "▶"
            else:
                col = C["white"]
                prefix = f"{i+1}."
            line(f"{prefix} {node['name']}", col)
        dist = state.get("tsp_dist", 0)
        line(f"Dist. ~{dist:.0f}", C["gray"])
    y += 4

    # ── Inventário ────────────────────────────────
    section("[ INVENTARIO ]")
    books = inventory.values()
    if not books:
        line("Vazio...", C["gray"])
    else:
        for book in books:
            line(f"  {book['name']}", book["color"])
    total_books = 4
    got = len(inventory)
    y += 4
    line(f"Livros: {got}/{total_books}",
         C["green"] if got == total_books else C["white"])

    if got == total_books:
        y += 4
        blit_text_center(surf, "TCC DESBLOQUEADO!",
                         sx + sw // 2, y, font_small, C["yellow"])
        y += 16

    # ── Controles ─────────────────────────────────
    y = sh - 90
    pygame.draw.line(surf, C["hud_border"], (sx + 4, y), (sx + sw - 4, y), 1)
    y += 6
    section("[ CONTROLES ]")
    for txt in ["Click: mover", "I: inventario", "ESC: sair"]:
        line(txt, C["gray"])


# ── Overlay de diálogo ─────────────────────────────────────────

def render_dialog_bg(surf, rect):
    overlay = pygame.Surface(rect[2:], pygame.SRCALPHA)
    overlay.fill(C["dialog_bg"])
    surf.blit(overlay, rect[:2])
    pygame.draw.rect(surf, C["hud_border"], rect, 3)


# ── Overlay escuro (tela de win, livro) ──────────────────────

def render_dark_overlay(surf, w, h, alpha=200):
    ov = pygame.Surface((w, h), pygame.SRCALPHA)
    ov.fill((6, 8, 14, alpha))
    surf.blit(ov, (0, 0))


# ── Scanlines CRT ────────────────────────────────────────────

def render_scanlines(surf, w, h):
    line_s = pygame.Surface((w, 1), pygame.SRCALPHA)
    line_s.fill((0, 0, 0, 18))
    for y in range(0, h, 3):
        surf.blit(line_s, (0, y))


# ── Tela de Vitória / Resultados ────────────────────────────────
def render_win_screen(surf, gs, w, h):
    surf.fill(C["bg"])
    cx = w // 2
    cy = h // 2

    # 1. Cálculo do Tempo (60 ticks = 1 segundo)
    segundos_totais = gs.tick // 60
    minutos = segundos_totais // 60
    segundos = segundos_totais % 60
    tempo_formatado = f"{minutos:02d}:{segundos:02d}"

    # 2. Contagem de Livros por Andar
    livros_por_andar = {}
    for andar in FLOORS:
        nome_curto = andar["name"].split("—")[0].strip() # Pega só "1º Andar"
        livros_por_andar[nome_curto] = 0

    # Verifica cada livro no inventário e encontra a qual andar pertence
    for book_id in gs.inventory.keys():
        for andar in FLOORS:
            for npc in andar["npcs"]:
                if npc["book_id"] == book_id:
                    nome_curto = andar["name"].split("—")[0].strip()
                    livros_por_andar[nome_curto] += 1

    # 3. Renderização dos Textos
    y = cy - 200
    blit_text_center(surf, "PARABENS, MESTRE DOS ALGORITMOS!", cx, y, font_large, C["yellow"])
    y += 30
    blit_text_center(surf, "Voce defendeu o seu TCC com sucesso e", cx, y, font_medium, C["white"])
    y += 20
    blit_text_center(surf, "coletou todo o conhecimento necessario!", cx, y, font_medium, C["white"])
    
    y += 50
    blit_text_center(surf, "── RESUMO DA JORNADA ──", cx, y, font_large, C["hud_text"])
    
    y += 40
    blit_text_center(surf, f"Tempo Total de Jogo: {tempo_formatado}", cx, y, font_medium, C["white"])
    y += 30
    blit_text_center(surf, f"Perguntas Certas: {gs.correct_answers}", cx, y, font_medium, C["green"])
    y += 30
    blit_text_center(surf, f"Perguntas Erradas: {gs.wrong_answers}", cx, y, font_medium, C["red"])
    
    y += 40
    blit_text_center(surf, "LIVROS COLETADOS:", cx, y, font_medium, C["yellow"])
    y += 25
    
    # Desenha as estatísticas de cada andar
    for andar, qtd in livros_por_andar.items():
        if qtd > 0:
            blit_text_center(surf, f"{andar}: {qtd} Livros", cx, y, font_small, C["book"])
            y += 20

    # Botão de Sair (Piscando)
    pulse = int(math.sin(gs.tick * 0.05) * 100) + 155 # Oscila entre 55 e 255
    cor_pisca = (pulse, pulse, pulse)
    y += 30
    blit_text_center(surf, "[ PRESSIONE ESC PARA SAIR ]", cx, y, font_medium, cor_pisca)