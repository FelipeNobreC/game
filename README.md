# AlgoQuest — Jogo Educativo de Algoritmos 🎓

Jogo educativo em **pixel art** que roda como janela nativa no seu sistema.

---

## 🛠️ Requisitos

- Python 3.10+ instalado
- pygame (`pip install pygame`)

---

## ▶️ Como executar

```bash
# Instalar dependência
pip install pygame

# Rodar o jogo
python main.py
```

---

## 🎮 Controles

| Ação | Controle |
|---|---|
| Mover personagem | **Clique esquerdo** no mapa |
| Abrir inventário | Tecla **I** |
| Sair | **ESC** |
| Pular texto | **Espaço** / clique em Continuar |

---

## 🧠 Estruturas de Dados Implementadas

### 1. HashMap (`hashmap.py`)
- Implementação from scratch com função hash polinomial de Bernstein
- Resolve colisões por **encadeamento**
- Rehash automático quando load factor ≥ 0.75
- Usado como **inventário de livros**: `HashMap<str, Livro>`
- Operações: `put`, `get`, `remove`, `has`, `values`, `keys`

### 2. Grafo de Grid + BFS (`graph.py`)
- Cada tile do mapa = **nó** do grafo
- Arestas = conexões ortogonais entre tiles transitáveis
- **BFS** garante caminho mínimo em grafos sem peso
- Usado para **pathfinding**: clique → personagem anda pela rota ótima
- Detecta obstáculos (paredes, portas fechadas)

### TSP — Heurística do Vizinho Mais Próximo (`graph.py`)
- Calcula rota ótima para visitar todos os professores do andar
- Heurística O(n²) — eficiente para n pequeno
- Exibido no HUD lateral em tempo real

---

## 📚 Conteúdos Educativos

| Andar | Professor | Tópico |
|---|---|---|
| 1 | Prof. Euler | TSP — Problema do Caixeiro Viajante |
| 1 | Prof. Hash | HashMap — Estrutura chave→valor |
| 2 | Prof. Dijkstra | Grafos e BFS/Dijkstra |
| 2 | Prof. Bellman | Mochila 0/1 — Programação Dinâmica |

---

## 📁 Estrutura de Arquivos

```
algoquest/
├── main.py        ← Entrada: loop principal, input, estados
├── data.py        ← Dados: andares, NPCs, perguntas, livros
├── hashmap.py     ← Estrutura de Dados #1: HashMap própria
├── graph.py       ← Estrutura de Dados #2: Grafo + BFS + TSP
├── renderer.py    ← Renderizador pixel art (pygame)
├── dialog.py      ← Sistema de diálogo, Q&A, typewriter
└── README.md      ← Este arquivo
```

---

## 🎯 Fluxo do Jogo

1. **Explore** os andares — clique no mapa para mover
2. **Encontre** os 2 professores de cada andar (5 salas, 2 com prof.)
3. **Aprenda** o conteúdo que o professor apresenta
4. **Responda** as perguntas para ganhar o livro
5. **Colete** o livro que cai no chão
6. **Suba** pelo elevador (desbloqueado após visitar os 2 professores)
7. **Complete** os 2 andares para craftear o TCC!
# game
