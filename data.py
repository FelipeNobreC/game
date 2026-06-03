# ============================================================
# data.py — Dados do jogo: fases, professores, perguntas, livros
# ============================================================

TILE = 32
COLS = 25
ROWS = 18

# ── Paleta pixel art ─────────────────────────────────────────
C = {
    "bg":           (10,  12,  20),
    "floor":        (22,  28,  44),
    "floor_alt":    (26,  33,  52),
    "wall":         (12,  14,  24),
    "wall_top":     (40,  52,  90),
    "wall_side":    (18,  22,  38),
    "door":         (80,  45,  20),
    "door_open":    (180, 110,  55),
    "door_frame":   (50,  30,  12),
    "carpet":       (20,  40,  32),
    "carpet_line":  (24,  50,  38),
    "elevator":     (28,  40,  70),
    "elev_on":      (50, 200, 160),
    "elev_off":     (40,  55,  90),
    "player":       (74, 247, 196),
    "player_body":  (30, 100, 140),
    "player_skin":  (220, 180, 140),
    "player_hair":  (80,  45,  15),
    "npc_body":     (40,  55,  80),
    "npc_hat":      (255, 200,  60),
    "book":         (255, 145,  50),
    "book_spine":   (180,  90,  20),
    "tsp_line":     (255,  60,  90, 120),
    "path_dot":     (74, 247, 196,  80),
    "hud_bg":       (10,  14,  22),
    "hud_border":   (74, 247, 196),
    "hud_text":     (74, 247, 196),
    "hud_dim":      (40,  60,  55),
    "white":        (255, 255, 255),
    "yellow":       (255, 204,  60),
    "red":          (255,  60,  60),
    "green":        (60, 220, 120),
    "gray":         (100, 120, 140),
    "dark":         (8,   10,  16),
    "overlay":      (8,   10,  18, 210),
    "dialog_bg":    (10,  16,  28, 230),
    "win_bg":       (6,    8,  14, 240),
}

# ── Mapa base ─────────────────────────────────────────────────
# 0=chão  1=parede  2=porta  3=elevador  4=carpete(sala)
def build_floor_map():
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            if r == 0 or r == ROWS-1 or c == 0 or c == COLS-1:
                row.append(1)
            else:
                row.append(0)
        grid.append(row)

    # Paredes do corredor (salas só no topo)
    for c in range(1, COLS-1):
        grid[6][c] = 1   # parede base das salas
        # corredor = linhas 7-10

    # 5 salas acima do corredor (linhas 1-5)
    # divisórias verticais entre salas
    room_dividers = [5, 10, 15, 20]
    for rd in room_dividers:
        for r in range(1, 7):
            grid[r][rd] = 1

    # Portas (centro de cada sala na linha 6)
    door_cols = [2, 7, 12, 17, 22]
    for dc in door_cols:
        grid[6][dc] = 2

    # Carpete interior das salas
    room_ranges = [(1,4), (6,9), (11,14), (16,19), (21,24)]
    for cs, ce in room_ranges:
        for r in range(1, 6):
            for c in range(cs, ce+1):
                grid[r][c] = 4

    # Elevador (canto inferior direito do corredor)
    for r in range(11, 14):
        for c in range(21, 24):
            grid[r][c] = 3

    # Parede separando elevador do corredor (com porta)
    for r in range(11, 14):
        grid[r][20] = 1
    grid[12][20] = 2  # porta do elevador

    return grid

# ── Definição dos andares ─────────────────────────────────────
FLOORS = [
    {
        "name": "1º Andar  —  Algoritmos Clássicos",
        "rooms": [
            {"id": "r1_1", "name": "Sala 101", "has_prof": False},
            {"id": "r1_2", "name": "Sala 102", "has_prof": True},
            {"id": "r1_3", "name": "Sala 103", "has_prof": False},
            {"id": "r1_4", "name": "Sala 104", "has_prof": True},
            {"id": "r1_5", "name": "Sala 105", "has_prof": False},
        ],
        "npcs": [
            {
                "id": "prof_tsp",
                "room_idx": 1,
                "tx": 7, "ty": 3,
                "name": "Prof. Euler",
                "topic": "TSP",
                "color": (255, 160, 60),
                "hat_color": (255, 200, 60),
                "book_id": "livro_tsp",
                "lines": [
                    "Olá! Sou o Prof. Euler.",
                    "Vou te ensinar sobre o TSP —",
                    "Problema do Caixeiro Viajante!",
                    "---",
                    "O TSP busca a ROTA MAIS CURTA",
                    "que visita todos os pontos",
                    "exatamente uma vez.",
                    "---",
                    "É NP-difícil: sem solução",
                    "eficiente exata para casos",
                    "grandes. Usamos heurísticas!",
                    "---",
                    "Neste jogo usamos o algoritmo",
                    "do VIZINHO MAIS PRÓXIMO para",
                    "calcular sua rota entre",
                    "os professores do andar.",
                ],
                "questions": [
                    {
                        "q": "O TSP pertence a qual\nclasse de complexidade?",
                        "options": ["P", "NP-difícil", "O(n log n)", "Linear"],
                        "correct": 1,
                        "explain": "TSP é NP-difícil! Não existe\nalgoritmo polinomial exato\nconhecido para ele.",
                    },
                    {
                        "q": "Qual heurística usamos\nno jogo para a rota?",
                        "options": ["Busca Binária", "Bubble Sort",
                                    "Viz. Mais Próximo", "DFS"],
                        "correct": 2,
                        "explain": "Vizinho Mais Próximo:\nsempre vá ao professor\nnão visitado mais próximo!",
                    },
                ],
            },
            {
                "id": "prof_hash",
                "room_idx": 3,
                "tx": 17, "ty": 3,
                "name": "Prof. Hash",
                "topic": "HashMap",
                "color": (160, 120, 255),
                "hat_color": (200, 160, 255),
                "book_id": "livro_hash",
                "lines": [
                    "Bem-vindo! Sou o Prof. Hash.",
                    "O inventário do jogo usa",
                    "exatamente uma HashMap!",
                    "---",
                    "HashMap armazena pares",
                    "CHAVE → VALOR.",
                    "---",
                    "A busca é O(1) em média",
                    "graças à função hash que",
                    "mapeia a chave ao índice.",
                    "---",
                    "No jogo: chave = nome do livro,",
                    "valor = objeto Livro.",
                    "Achar qualquer livro é",
                    "instantâneo!",
                ],
                "questions": [
                    {
                        "q": "Complexidade média\nde busca numa HashMap?",
                        "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"],
                        "correct": 2,
                        "explain": "HashMap tem busca O(1)!\nA função hash mapeia a chave\ndiretamente à posição.",
                    },
                    {
                        "q": "O que é uma COLISÃO\nna HashMap?",
                        "options": [
                            "Valores iguais",
                            "Duas chaves, mesmo hash",
                            "Lista cheia",
                            "Erro de memória",
                        ],
                        "correct": 1,
                        "explain": "Colisão: duas chaves diferentes\ngeram o mesmo índice hash.\nResolvemos com encadeamento!",
                    },
                ],
            },
        ],
    },
    {
        "name": "2º Andar  —  Grafos e Busca",
        "rooms": [
            {"id": "r2_1", "name": "Sala 201", "has_prof": False},
            {"id": "r2_2", "name": "Sala 202", "has_prof": False},
            {"id": "r2_3", "name": "Sala 203", "has_prof": True},
            {"id": "r2_4", "name": "Sala 204", "has_prof": False},
            {"id": "r2_5", "name": "Sala 205", "has_prof": True},
        ],
        "npcs": [
            {
                "id": "prof_graph",
                "room_idx": 2,
                "tx": 12, "ty": 3,
                "name": "Prof. Dijkstra",
                "topic": "Grafos / BFS",
                "color": (60, 200, 255),
                "hat_color": (120, 220, 255),
                "book_id": "livro_graph",
                "lines": [
                    "Olá! Sou o Prof. Dijkstra.",
                    "O pathfinding do personagem",
                    "usa BFS num grafo de grid!",
                    "---",
                    "Um GRAFO tem nós e arestas.",
                    "No jogo cada TILE é um nó;",
                    "vizinhos ortogonais = arestas.",
                    "---",
                    "BFS (Busca em Largura) garante",
                    "o caminho MÍNIMO em grafos",
                    "sem peso (ou peso uniforme).",
                    "---",
                    "Dijkstra generaliza para",
                    "grafos com pesos variados.",
                    "Essencial em GPS e redes!",
                ],
                "questions": [
                    {
                        "q": "Cada TILE do mapa\nrepresenta o quê no grafo?",
                        "options": ["Uma aresta", "Um nó", "Uma função hash", "Uma pilha"],
                        "correct": 1,
                        "explain": "Cada tile é um nó!\nAs arestas conectam tiles\nadjacentes transitáveis.",
                    },
                    {
                        "q": "BFS garante caminho\nmínimo em grafos:",
                        "options": [
                            "Com pesos negativos",
                            "Sem peso (uniforme)",
                            "Só em árvores",
                            "Com peso exponencial",
                        ],
                        "correct": 1,
                        "explain": "BFS = mínimo em grafos\nsem peso. Para pesos\nvariados, use Dijkstra!",
                    },
                ],
            },
            {
                "id": "prof_knapsack",
                "room_idx": 4,
                "tx": 22, "ty": 3,
                "name": "Prof. Bellman",
                "topic": "Mochila / DP",
                "color": (255, 100, 140),
                "hat_color": (255, 150, 180),
                "book_id": "livro_knapsack",
                "lines": [
                    "Olá! Sou o Prof. Bellman.",
                    "Você coleta livros — isso é",
                    "o Problema da Mochila!",
                    "---",
                    "Dado itens com peso e valor,",
                    "maximize o valor total sem",
                    "exceder a capacidade.",
                    "---",
                    "Resolve com PROGRAMAÇÃO",
                    "DINÂMICA em O(n · W).",
                    "Evita recalcular subproblemas",
                    "já resolvidos!",
                    "---",
                    "No jogo: cada livro é um item,",
                    "conhecimento é o valor,",
                    "e sua mochila é a capacidade.",
                ],
                "questions": [
                    {
                        "q": "Mochila 0/1 é resolvida\neficientemente com:",
                        "options": ["Força Bruta", "Prog. Dinâmica", "Bubble Sort", "DFS"],
                        "correct": 1,
                        "explain": "Programação Dinâmica!\nO(n·W) — evita recalcular\nsubproblemas repetidos.",
                    },
                    {
                        "q": "Na versão 0/1, cada\nitem pode ser:",
                        "options": [
                            "Dividido em frações",
                            "Incluído ou excluído",
                            "Repetido infinitamente",
                            "Ordenado por peso",
                        ],
                        "correct": 1,
                        "explain": "0/1 = incluir (1) ou não (0).\nSem frações! A versão\nfracionária é mais simples.",
                    },
                ],
            },
        ],
    },
    # ── 3º Andar ──────────────────────────────────────────────
    {
        "name": "3º Andar  —  Ordenação",
        "rooms": [
            {"id": "r3_1", "name": "Sala 301", "has_prof": True},
            {"id": "r3_2", "name": "Sala 302", "has_prof": False},
            {"id": "r3_3", "name": "Sala 303", "has_prof": False},
            {"id": "r3_4", "name": "Sala 304", "has_prof": True},
            {"id": "r3_5", "name": "Sala 305", "has_prof": False},
        ],
        "npcs": [
            {
                "id": "prof_quick",
                "room_idx": 0,
                "tx": 2, "ty": 3,
                "name": "Prof. Quick",
                "topic": "QuickSort",
                "color": (255, 80, 80),
                "hat_color": (255, 130, 60),
                "book_id": "livro_quicksort",
                "lines": [
                    "Olá! Sou o Prof. Quick.",
                    "Vou te ensinar o QuickSort —",
                    "um dos mais usados na prática!",
                    "---",
                    "QuickSort escolhe um PIVOT",
                    "e particiona o array:",
                    "menores à esq, maiores à dir.",
                    "---",
                    "Depois aplica recursão em",
                    "cada metade. Elegante, né?",
                    "---",
                    "Média: O(n log n).",
                    "Pior caso: O(n²) quando o",
                    "pivot é sempre o menor ou",
                    "maior elemento (lista sorted).",
                ],
                "questions": [
                    {
                        "q": "Complexidade MÉDIA\ndo QuickSort?",
                        "options": ["O(n²)", "O(n log n)", "O(log n)", "O(n)"],
                        "correct": 1,
                        "explain": "QuickSort tem média O(n log n)!\nCom pivot aleatório o pior\ncaso é extremamente raro.",
                    },
                    {
                        "q": "O pior caso do QuickSort\nocorre quando o pivot é:",
                        "options": [
                            "O elemento do meio",
                            "Aleatório",
                            "Sempre o menor/maior",
                            "A mediana",
                        ],
                        "correct": 2,
                        "explain": "Pivot sempre extremo gera\npartições 1 e n-1: O(n²).\nMediana de 3 evita isso!",
                    },
                ],
            },
            {
                "id": "prof_merge",
                "room_idx": 3,
                "tx": 17, "ty": 3,
                "name": "Prof. Merge",
                "topic": "MergeSort",
                "color": (80, 200, 120),
                "hat_color": (120, 240, 160),
                "book_id": "livro_mergesort",
                "lines": [
                    "Bem-vindo! Sou o Prof. Merge.",
                    "O MergeSort garante O(n log n)",
                    "em TODOS os casos!",
                    "---",
                    "Estratégia: DIVISÃO E CONQUISTA.",
                    "Divide o array ao meio,",
                    "ordena cada parte,",
                    "depois MESCLA os resultados.",
                    "---",
                    "É um algoritmo ESTÁVEL:",
                    "elementos iguais mantêm",
                    "a ordem relativa original.",
                    "---",
                    "Custo extra: O(n) de memória",
                    "auxiliar para a mesclagem.",
                ],
                "questions": [
                    {
                        "q": "MergeSort tem qual\ncomplexidade no PIOR caso?",
                        "options": ["O(n²)", "O(n)", "O(n log n)", "O(log n)"],
                        "correct": 2,
                        "explain": "MergeSort é sempre O(n log n)!\nMelhor, médio e pior caso.\nIsso o diferencia do QuickSort.",
                    },
                    {
                        "q": "MergeSort é classificado\ncomo algoritmo de:",
                        "options": [
                            "Força Bruta",
                            "Divisão e Conquista",
                            "Programação Dinâmica",
                            "Algoritmo Guloso",
                        ],
                        "correct": 1,
                        "explain": "Divide e Conquista!\nDivide o problema em partes\nmenores e combina os resultados.",
                    },
                ],
            },
        ],
    },
    # ── 4º Andar ──────────────────────────────────────────────
    {
        "name": "4º Andar  —  Árvores",
        "rooms": [
            {"id": "r4_1", "name": "Sala 401", "has_prof": False},
            {"id": "r4_2", "name": "Sala 402", "has_prof": True},
            {"id": "r4_3", "name": "Sala 403", "has_prof": False},
            {"id": "r4_4", "name": "Sala 404", "has_prof": False},
            {"id": "r4_5", "name": "Sala 405", "has_prof": True},
        ],
        "npcs": [
            {
                "id": "prof_knuth",
                "room_idx": 1,
                "tx": 7, "ty": 3,
                "name": "Prof. Knuth",
                "topic": "BST / AVL",
                "color": (255, 220, 60),
                "hat_color": (255, 240, 120),
                "book_id": "livro_bst",
                "lines": [
                    "Olá! Sou o Prof. Knuth.",
                    "Vamos falar sobre Árvores",
                    "Binárias de Busca — BST!",
                    "---",
                    "Numa BST: filho esquerdo",
                    "< nó pai < filho direito.",
                    "Isso permite busca em O(log n)!",
                    "---",
                    "Mas se a árvore ficar",
                    "desbalanceada, a busca",
                    "degrada para O(n).",
                    "---",
                    "Solução: AVL Tree!",
                    "Rebalanceia automaticamente",
                    "garantindo sempre O(log n).",
                ],
                "questions": [
                    {
                        "q": "Busca em BST balanceada\ntem complexidade:",
                        "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
                        "correct": 2,
                        "explain": "BST balanceada: O(log n)!\nCada comparação descarta\nmetade dos nós restantes.",
                    },
                    {
                        "q": "A AVL Tree garante\ndesempenho O(log n) pois:",
                        "options": [
                            "Usa tabela hash interna",
                            "Mantém a árvore balanceada",
                            "Ordena os nós em array",
                            "Usa busca binária",
                        ],
                        "correct": 1,
                        "explain": "AVL rebalanceia após\ncada inserção/remoção!\nFator de balanceamento ≤ 1.",
                    },
                ],
            },
            {
                "id": "prof_heap",
                "room_idx": 4,
                "tx": 22, "ty": 3,
                "name": "Prof. Heap",
                "topic": "Heap / Fila de Prioridade",
                "color": (200, 100, 255),
                "hat_color": (220, 150, 255),
                "book_id": "livro_heap",
                "lines": [
                    "Olá! Sou o Prof. Heap.",
                    "Um Heap é uma árvore binária",
                    "com uma propriedade especial!",
                    "---",
                    "MAX-HEAP: cada nó é MAIOR",
                    "ou igual aos seus filhos.",
                    "A raiz = maior elemento!",
                    "---",
                    "MIN-HEAP: cada nó é MENOR",
                    "ou igual aos seus filhos.",
                    "A raiz = menor elemento!",
                    "---",
                    "Inserção e remoção: O(log n).",
                    "Usado em filas de prioridade",
                    "e no algoritmo HeapSort!",
                ],
                "questions": [
                    {
                        "q": "Num Max-Heap, a raiz\ncontém sempre:",
                        "options": [
                            "O menor elemento",
                            "O elemento do meio",
                            "O maior elemento",
                            "Um elemento aleatório",
                        ],
                        "correct": 2,
                        "explain": "Raiz do Max-Heap = máximo!\nPropriedade: pai ≥ filhos\nem toda a árvore.",
                    },
                    {
                        "q": "Inserção num Heap\ntem complexidade:",
                        "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
                        "correct": 2,
                        "explain": "Inserção no Heap: O(log n)!\nInsere na folha e faz\n'sift-up' até restaurar heap.",
                    },
                ],
            },
        ],
    },
    # ── 5º Andar ──────────────────────────────────────────────
    {
        "name": "5º Andar  —  Algoritmos Gulosos",
        "rooms": [
            {"id": "r5_1", "name": "Sala 501", "has_prof": False},
            {"id": "r5_2", "name": "Sala 502", "has_prof": False},
            {"id": "r5_3", "name": "Sala 503", "has_prof": True},
            {"id": "r5_4", "name": "Sala 504", "has_prof": False},
            {"id": "r5_5", "name": "Sala 505", "has_prof": True},
        ],
        "npcs": [
            {
                "id": "prof_prim",
                "room_idx": 2,
                "tx": 12, "ty": 3,
                "name": "Prof. Prim",
                "topic": "Árvore Geradora Mínima",
                "color": (60, 220, 200),
                "hat_color": (100, 240, 220),
                "book_id": "livro_mst",
                "lines": [
                    "Olá! Sou o Prof. Prim.",
                    "Falarei sobre a Árvore",
                    "Geradora Mínima — MST!",
                    "---",
                    "Dado um grafo ponderado,",
                    "a MST conecta todos os",
                    "vértices com MENOR custo total.",
                    "---",
                    "Algoritmo de Prim: começa",
                    "num vértice e adiciona sempre",
                    "a ARESTA de menor peso",
                    "que expande a árvore.",
                    "---",
                    "Kruskal: ordena as arestas",
                    "e adiciona sem criar ciclos.",
                    "Ambos são GULOSOS!",
                ],
                "questions": [
                    {
                        "q": "A MST de um grafo com\nV vértices tem quantas arestas?",
                        "options": ["V", "V + 1", "V - 1", "V²"],
                        "correct": 2,
                        "explain": "MST tem sempre V-1 arestas!\nConecta V vértices sem ciclos\n= árvore = V-1 arestas.",
                    },
                    {
                        "q": "Prim e Kruskal são\nexemplos de algoritmos:",
                        "options": [
                            "Divisão e Conquista",
                            "Prog. Dinâmica",
                            "Gulosos (Greedy)",
                            "Backtracking",
                        ],
                        "correct": 2,
                        "explain": "Ambos são gulosos!\nFazem sempre a escolha\nlocalmente ótima a cada passo.",
                    },
                ],
            },
            {
                "id": "prof_huffman",
                "room_idx": 4,
                "tx": 22, "ty": 3,
                "name": "Prof. Huffman",
                "topic": "Compressão Huffman",
                "color": (255, 160, 40),
                "hat_color": (255, 200, 80),
                "book_id": "livro_huffman",
                "lines": [
                    "Olá! Sou o Prof. Huffman.",
                    "A compressão Huffman é um",
                    "algoritmo GULOSO elegante!",
                    "---",
                    "Ideia: caracteres MAIS COMUNS",
                    "recebem códigos binários",
                    "MAIS CURTOS.",
                    "---",
                    "Constrói uma árvore a partir",
                    "de frequências: os dois nós",
                    "de menor frequência são",
                    "unidos a cada passo.",
                    "---",
                    "Resultado: compressão sem perda",
                    "usada em ZIP, JPEG e MP3!",
                ],
                "questions": [
                    {
                        "q": "No Huffman, caracteres\nmais frequentes recebem:",
                        "options": [
                            "Códigos mais longos",
                            "Códigos iguais",
                            "Códigos mais curtos",
                            "Sem código",
                        ],
                        "correct": 2,
                        "explain": "Mais frequente = código menor!\nIsso reduz o tamanho total.\nÉ a essência da compressão.",
                    },
                    {
                        "q": "Huffman é classificado\ncomo algoritmo:",
                        "options": [
                            "Prog. Dinâmica",
                            "Guloso (Greedy)",
                            "Divisão e Conquista",
                            "Força Bruta",
                        ],
                        "correct": 1,
                        "explain": "Huffman é guloso!\nSempre une os dois nós\nde menor frequência.",
                    },
                ],
            },
        ],
    },
    # ── 6º Andar ──────────────────────────────────────────────
    {
        "name": "6º Andar  —  Programação Dinâmica Avançada",
        "rooms": [
            {"id": "r6_1", "name": "Sala 601", "has_prof": True},
            {"id": "r6_2", "name": "Sala 602", "has_prof": False},
            {"id": "r6_3", "name": "Sala 603", "has_prof": False},
            {"id": "r6_4", "name": "Sala 604", "has_prof": True},
            {"id": "r6_5", "name": "Sala 605", "has_prof": False},
        ],
        "npcs": [
            {
                "id": "prof_levenshtein",
                "room_idx": 0,
                "tx": 2, "ty": 3,
                "name": "Prof. Levenshtein",
                "topic": "Distância de Edição",
                "color": (120, 200, 80),
                "hat_color": (160, 230, 100),
                "book_id": "livro_edit_dist",
                "lines": [
                    "Olá! Sou Prof. Levenshtein.",
                    "A Distância de Edição mede",
                    "o quanto duas strings diferem!",
                    "---",
                    "Três operações permitidas:",
                    "INSERIR, DELETAR ou",
                    "SUBSTITUIR um caractere.",
                    "---",
                    "Ex: 'gato' → 'pato' = 1",
                    "(substituição de g por p)",
                    "---",
                    "Resolvemos com DP em O(m·n),",
                    "construindo uma tabela onde",
                    "dp[i][j] = edições para",
                    "transformar s1[0..i] em s2[0..j].",
                ],
                "questions": [
                    {
                        "q": "Quantas operações define\na Distância de Edição?",
                        "options": ["1 (substituição)", "2 (ins. e del.)", "3 (ins, del, subst)", "4"],
                        "correct": 2,
                        "explain": "Inserção, Deleção e Substituição!\nCada uma conta como 1 edição.\nBusca-se o mínimo de operações.",
                    },
                    {
                        "q": "Complexidade da Distância\nde Edição com DP?",
                        "options": ["O(m + n)", "O(m · n)", "O(m log n)", "O(2ⁿ)"],
                        "correct": 1,
                        "explain": "O(m·n) preenchendo\numa tabela m×n.\nMuito melhor que força bruta!",
                    },
                ],
            },
            {
                "id": "prof_floyd",
                "room_idx": 3,
                "tx": 17, "ty": 3,
                "name": "Prof. Floyd",
                "topic": "Floyd-Warshall",
                "color": (100, 160, 255),
                "hat_color": (140, 190, 255),
                "book_id": "livro_floyd",
                "lines": [
                    "Olá! Sou o Prof. Floyd.",
                    "O algoritmo Floyd-Warshall",
                    "resolve os CAMINHOS MÍNIMOS",
                    "entre TODOS os pares!",
                    "---",
                    "Dijkstra resolve de 1 fonte.",
                    "Floyd-Warshall resolve",
                    "todos os V² pares de uma vez.",
                    "---",
                    "Usa Programação Dinâmica:",
                    "dp[i][j] = menor caminho",
                    "de i até j usando nós 1..k.",
                    "---",
                    "Complexidade: O(V³).",
                    "Funciona até com arestas",
                    "de peso NEGATIVO!",
                ],
                "questions": [
                    {
                        "q": "Floyd-Warshall resolve\ncaminhos mínimos entre:",
                        "options": [
                            "Um par específico",
                            "Uma origem e todos",
                            "Todos os pares (V²)",
                            "Só grafos sem peso",
                        ],
                        "correct": 2,
                        "explain": "Floyd-Warshall = todos os pares!\nCalcula dist[i][j] para\ncada combinação de vértices.",
                    },
                    {
                        "q": "Complexidade do\nFloyd-Warshall?",
                        "options": ["O(V²)", "O(V log V)", "O(V³)", "O(E log V)"],
                        "correct": 2,
                        "explain": "O(V³): três loops aninhados\nsobre todos os vértices.\nViável para grafos pequenos.",
                    },
                ],
            },
        ],
    },
    # ── 7º Andar ──────────────────────────────────────────────
    {
        "name": "7º Andar  —  Complexidade e Backtracking",
        "rooms": [
            {"id": "r7_1", "name": "Sala 701", "has_prof": False},
            {"id": "r7_2", "name": "Sala 702", "has_prof": True},
            {"id": "r7_3", "name": "Sala 703", "has_prof": False},
            {"id": "r7_4", "name": "Sala 704", "has_prof": True},
            {"id": "r7_5", "name": "Sala 705", "has_prof": False},
        ],
        "npcs": [
            {
                "id": "prof_turing",
                "room_idx": 1,
                "tx": 7, "ty": 3,
                "name": "Prof. Turing",
                "topic": "P vs NP",
                "color": (220, 80, 200),
                "hat_color": (240, 120, 220),
                "book_id": "livro_complexity",
                "lines": [
                    "Olá! Sou o Prof. Turing.",
                    "Falaremos sobre a MAIOR",
                    "questão em aberto da CC!",
                    "---",
                    "Classe P: problemas que",
                    "se RESOLVEM em tempo polinomial.",
                    "---",
                    "Classe NP: problemas cuja",
                    "solução se VERIFICA em",
                    "tempo polinomial.",
                    "---",
                    "A pergunta: P = NP?",
                    "Se sim, tudo que podemos",
                    "verificar, podemos resolver!",
                    "Premio: 1 milhão de dólares!",
                ],
                "questions": [
                    {
                        "q": "Classe P contém problemas\nque podem ser:",
                        "options": [
                            "Verificados em O(n)",
                            "Resolvidos em tempo polinomial",
                            "Somente aproximados",
                            "Indecidíveis",
                        ],
                        "correct": 1,
                        "explain": "P = decidíveis em tempo\npolinomial (O(nᵏ)).\nExemplos: ordenação, BFS.",
                    },
                    {
                        "q": "Em NP, 'verificar' a\nsolução é feito em:",
                        "options": [
                            "Tempo exponencial",
                            "Tempo polinomial",
                            "Tempo constante",
                            "Não é possível",
                        ],
                        "correct": 1,
                        "explain": "NP: verificação polinomial!\nO difícil é ENCONTRAR a solução,\nnão confirmar se ela é válida.",
                    },
                ],
            },
            {
                "id": "prof_cook",
                "room_idx": 3,
                "tx": 17, "ty": 3,
                "name": "Prof. Cook",
                "topic": "Backtracking",
                "color": (255, 120, 80),
                "hat_color": (255, 160, 100),
                "book_id": "livro_backtracking",
                "lines": [
                    "Olá! Sou o Prof. Cook.",
                    "Backtracking é uma técnica",
                    "de busca sistemática!",
                    "---",
                    "Constrói a solução passo a",
                    "passo. Se chegar a beco",
                    "sem saída, VOLTA (backtrack)",
                    "e tenta outro caminho.",
                    "---",
                    "Exemplos clássicos:",
                    "N-Rainhas, Sudoku,",
                    "Subconjuntos e labirintos.",
                    "---",
                    "É força bruta inteligente:",
                    "a PODA elimina ramos",
                    "inviáveis mais cedo!",
                ],
                "questions": [
                    {
                        "q": "Backtracking difere da\nforça bruta pois adiciona:",
                        "options": [
                            "Memoização",
                            "Poda de ramos inviáveis",
                            "Ordenação prévia",
                            "Hashing",
                        ],
                        "correct": 1,
                        "explain": "Poda (pruning)!\nDescarta ramos que não\npodem levar à solução.",
                    },
                    {
                        "q": "Qual problema é clássico\nde Backtracking?",
                        "options": [
                            "Ordenação",
                            "Busca Binária",
                            "N-Rainhas",
                            "Floyd-Warshall",
                        ],
                        "correct": 2,
                        "explain": "N-Rainhas: posicionar N rainhas\nnum tabuleiro N×N sem que\nnenhuma se ataque.",
                    },
                ],
            },
        ],
    },
]

# ── Livros ────────────────────────────────────────────────────
BOOKS = {
    "livro_tsp": {
        "id": "livro_tsp",
        "name": "1° Período: TSP",
        "color": (255, 145, 50),
        "desc": [
            "Traveling Salesman Problem",
            "Classe: NP-difícil",
            "Heurística: Vizinho Mais Próximo",
            "O(n²) para a heurística",
        ],
        "qa": [("Classe do TSP?", "NP-difícil"),
               ("Heurística do jogo?", "Vizinho Mais Próximo")],
    },
    "livro_hash": {
        "id": "livro_hash",
        "name": "2° Período: HashMap",
        "color": (160, 120, 255),
        "desc": [
            "HashMap: chave → valor",
            "Busca média: O(1)",
            "Colisão: mesma posição hash",
            "Resolução: encadeamento",
        ],
        "qa": [("Busca na HashMap?", "O(1) em média"),
               ("O que é colisão?", "Duas chaves, mesmo hash")],
    },
    "livro_graph": {
        "id": "livro_graph",
        "name": "3° Período: Grafos",
        "color": (60, 200, 255),
        "desc": [
            "Grafo: nós + arestas",
            "BFS: caminho mínimo s/ peso",
            "Dijkstra: grafos com peso",
            "Grid = grafo implícito",
        ],
        "qa": [("Tile = ?", "Nó do grafo"),
               ("BFS funciona em grafos?", "Sem peso (ou uniforme)")],
    },
    "livro_knapsack": {
        "id": "livro_knapsack",
        "name": "4° Período: Mochila",
        "color": (255, 100, 140),
        "desc": [
            "Knapsack 0/1: maximizar valor",
            "Técnica: Prog. Dinâmica",
            "Complexidade: O(n · W)",
            "0/1: inclui ou exclui o item",
        ],
        "qa": [("Técnica de solução?", "Programação Dinâmica"),
               ("Versão 0/1?", "Incluir ou excluir o item")],
    },
    "livro_quicksort": {
        "id": "livro_quicksort",
        "name": "5° Período: QuickSort",
        "color": (255, 80, 80),
        "desc": [
            "QuickSort: pivot + particionamento",
            "Média: O(n log n)",
            "Pior caso: O(n²) - pivot extremo",
            "In-place: não usa memória extra",
        ],
        "qa": [("Complexidade média?", "O(n log n)"),
               ("Quando ocorre pior caso?", "Pivot sempre extremo")],
    },
    "livro_mergesort": {
        "id": "livro_mergesort",
        "name": "6° Período: MergeSort",
        "color": (80, 200, 120),
        "desc": [
            "MergeSort: Divisão e Conquista",
            "Sempre O(n log n) - estável",
            "Memória extra: O(n)",
            "Ideal para dados externos",
        ],
        "qa": [("Complexidade no pior caso?", "O(n log n)"),
               ("Paradigma usado?", "Divisão e Conquista")],
    },
    "livro_bst": {
        "id": "livro_bst",
        "name": "7° Período: BST / AVL",
        "color": (255, 220, 60),
        "desc": [
            "BST: esq < pai < dir",
            "Busca balanceada: O(log n)",
            "AVL: auto-balanceada",
            "Desbalanceada degenera em O(n)",
        ],
        "qa": [("Busca em BST balanceada?", "O(log n)"),
               ("AVL garante o quê?", "Árvore sempre balanceada")],
    },
    "livro_heap": {
        "id": "livro_heap",
        "name": "8° Período: Heap",
        "color": (200, 100, 255),
        "desc": [
            "Max-Heap: raiz = maior elemento",
            "Min-Heap: raiz = menor elemento",
            "Inserção/remoção: O(log n)",
            "Base do HeapSort e fila de prioridade",
        ],
        "qa": [("Raiz do Max-Heap?", "Maior elemento"),
               ("Complexidade de inserção?", "O(log n)")],
    },
    "livro_mst": {
        "id": "livro_mst",
        "name": "9° Período: MST",
        "color": (60, 220, 200),
        "desc": [
            "MST: conecta V vértices com min custo",
            "Número de arestas: V - 1",
            "Prim e Kruskal: algoritmos gulosos",
            "Aplicação: redes e infraestrutura",
        ],
        "qa": [("Arestas na MST?", "V - 1"),
               ("Prim e Kruskal são?", "Algoritmos Gulosos")],
    },
    "livro_huffman": {
        "id": "livro_huffman",
        "name": "10° Período: Huffman",
        "color": (255, 160, 40),
        "desc": [
            "Huffman: compressão sem perda",
            "Mais frequente = código menor",
            "Paradigma: Guloso",
            "Usado em ZIP, JPEG, MP3",
        ],
        "qa": [("Huffman é que tipo de algoritmo?", "Guloso (Greedy)"),
               ("Frequente ganha código?", "Mais curto")],
    },
    "livro_edit_dist": {
        "id": "livro_edit_dist",
        "name": "11° Período: Dist. Edição",
        "color": (120, 200, 80),
        "desc": [
            "3 ops: inserção, deleção, substituição",
            "DP: tabela m×n",
            "Complexidade: O(m · n)",
            "Usado em corretores ortográficos",
        ],
        "qa": [("Operações permitidas?", "Inserção, deleção, substituição"),
               ("Complexidade com DP?", "O(m · n)")],
    },
    "livro_floyd": {
        "id": "livro_floyd",
        "name": "12° Período: Floyd-Warshall",
        "color": (100, 160, 255),
        "desc": [
            "Todos os pares de caminhos mínimos",
            "Complexidade: O(V³)",
            "Funciona com pesos negativos",
            "Paradigma: Prog. Dinâmica",
        ],
        "qa": [("Resolve caminhos entre?", "Todos os pares de vértices"),
               ("Complexidade?", "O(V³)")],
    },
    "livro_complexity": {
        "id": "livro_complexity",
        "name": "13° Período: P vs NP",
        "color": (220, 80, 200),
        "desc": [
            "P: resolve em tempo polinomial",
            "NP: verifica em tempo polinomial",
            "P = NP? Questão em aberto",
            "NP-Completo: mais difíceis de NP",
        ],
        "qa": [("Classe P significa?", "Resolve em tempo polinomial"),
               ("NP verificar é feito em?", "Tempo polinomial")],
    },
    "livro_backtracking": {
        "id": "livro_backtracking",
        "name": "14° Período: Backtracking",
        "color": (255, 120, 80),
        "desc": [
            "Busca sistemática com retrocesso",
            "Poda: elimina ramos inviáveis",
            "Exemplos: N-Rainhas, Sudoku",
            "Força bruta com inteligência",
        ],
        "qa": [("Backtracking adiciona o quê?", "Poda de ramos inviáveis"),
               ("Clássico do backtracking?", "N-Rainhas")],
    },
}

# Posições das salas (col_start, col_end)
ROOM_RANGES = [(1, 4), (6, 9), (11, 14), (16, 19), (21, 24)]
DOOR_COLS   = [2, 7, 12, 17, 22]
