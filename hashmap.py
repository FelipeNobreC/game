# ============================================================
# hashmap.py — Estrutura de Dados #1: HashMap<str, Livro>
# Implementação própria com função hash polinomial
# ============================================================

class HashMap:
    """
    HashMap com encadeamento para resolução de colisões.
    Usado como inventário: HashMap<str, dict(Livro)>
    """

    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.size = 0
        self.load_factor = 0.75
        self._buckets: list[list] = [[] for _ in range(self.capacity)]

    # ── Função hash polinomial (Bernstein) ───────────────────
    def _hash(self, key: str) -> int:
        h = 5381
        for ch in key:
            h = (h * 33 + ord(ch)) % self.capacity
        return h

    # ── Rehash quando load factor é excedido ─────────────────
    def _rehash(self):
        old_buckets = self._buckets
        self.capacity *= 2
        self._buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)

    # ── PUT — O(1) amortizado ─────────────────────────────────
    def put(self, key: str, value) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._rehash()
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return
        self._buckets[idx].append([key, value])
        self.size += 1

    # ── GET — O(1) amortizado ─────────────────────────────────
    def get(self, key: str):
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    # ── REMOVE ────────────────────────────────────────────────
    def remove(self, key: str) -> bool:
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    # ── HAS ──────────────────────────────────────────────────
    def has(self, key: str) -> bool:
        return self.get(key) is not None

    # ── VALUES ───────────────────────────────────────────────
    def values(self) -> list:
        result = []
        for bucket in self._buckets:
            for _, v in bucket:
                result.append(v)
        return result

    # ── KEYS ─────────────────────────────────────────────────
    def keys(self) -> list:
        result = []
        for bucket in self._buckets:
            for k, _ in bucket:
                result.append(k)
        return result

    # ── Iteração ──────────────────────────────────────────────
    def items(self):
        for bucket in self._buckets:
            for k, v in bucket:
                yield k, v

    def __len__(self):
        return self.size

    def __repr__(self):
        pairs = [(k, v) for k, v in self.items()]
        return f"HashMap(size={self.size}, cap={self.capacity}, items={pairs})"
