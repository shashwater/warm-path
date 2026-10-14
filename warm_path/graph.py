"""Relationship graph + warmest-intro-path search.

Edge strength in (0, 1] is built from interaction history: more interactions,
more recent, and two-way interactions all make a tie warmer. The warmest path
to a target maximizes the product of edge strengths (with a small penalty per
hop), which is a shortest path on -log(strength).
"""
import csv
import heapq
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import date

HALF_LIFE_DAYS = 365.0
HOP_PENALTY = 0.85  # each extra intro hop costs 15% warmth
KIND_WEIGHT = {"meeting": 1.0, "call": 0.8, "email": 0.4, "message": 0.3, "coworker": 1.2, "intro": 1.0}


@dataclass(frozen=True)
class Interaction:
    a: str
    b: str
    kind: str
    when: date
    two_way: bool = True


def edge_strength(interactions, today):
    """Squash a list of interactions between two people into a strength in (0, 1)."""
    score = 0.0
    for i in interactions:
        age = max((today - i.when).days, 0)
        decay = 0.5 ** (age / HALF_LIFE_DAYS)
        w = KIND_WEIGHT.get(i.kind, 0.3) * (1.0 if i.two_way else 0.4)
        score += w * decay
    return 1.0 - math.exp(-score)  # diminishing returns


class Graph:
    def __init__(self):
        self._inter = defaultdict(list)
        self.people = set()

    def add(self, i: Interaction):
        key = tuple(sorted((i.a, i.b)))
        self._inter[key].append(i)
        self.people.update(key)

    def strengths(self, today):
        out = defaultdict(dict)
        for (a, b), items in self._inter.items():
            s = edge_strength(items, today)
            out[a][b] = s
            out[b][a] = s
        return out

    def warmest_path(self, source, target, today, max_hops=3):
        """Return (path, warmth) or (None, 0.0). Warmth is the product of
        edge strengths times HOP_PENALTY per intermediary."""
        if source not in self.people or target not in self.people:
            return None, 0.0
        adj = self.strengths(today)
        # state: (cost, node, hops, path)
        heap = [(0.0, source, 0, [source])]
        best = {}
        while heap:
            cost, node, hops, path = heapq.heappop(heap)
            if node == target:
                return path, math.exp(-cost)
            if best.get((node, hops), math.inf) <= cost:
                continue
            best[(node, hops)] = cost
            if hops >= max_hops:
                continue
            for nxt, s in adj[node].items():
                if nxt in path or s <= 0:
                    continue
                step = -math.log(s) - (math.log(HOP_PENALTY) if hops >= 1 else 0.0)
                heapq.heappush(heap, (cost + step, nxt, hops + 1, path + [nxt]))
        return None, 0.0

    def top_paths(self, source, targets, today, max_hops=3):
        rows = []
        for t in targets:
            p, w = self.warmest_path(source, t, today, max_hops)
            if p:
                rows.append((t, p, w))
        return sorted(rows, key=lambda r: -r[2])


def load_csv(path):
    """CSV columns: a,b,kind,date(YYYY-MM-DD),two_way(0/1)"""
    g = Graph()
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            g.add(Interaction(r["a"].strip(), r["b"].strip(), r["kind"].strip(),
                              date.fromisoformat(r["date"]), r.get("two_way", "1") != "0"))
    return g
