from datetime import date
from warm_path import Graph, Interaction, edge_strength
from warm_path.intro import intro_ask

T = date(2026, 10, 14)

def I(a, b, k="meeting", d=date(2026, 10, 1), tw=True):
    return Interaction(a, b, k, d, tw)

def test_recent_beats_old():
    assert edge_strength([I("a", "b")], T) > edge_strength([I("a", "b", d=date(2022, 1, 1))], T)

def test_two_way_beats_one_way():
    assert edge_strength([I("a", "b")], T) > edge_strength([I("a", "b", tw=False)], T)

def test_strength_bounded():
    s = edge_strength([I("a", "b")] * 5, T)
    assert 0 < s < 1

def test_prefers_warm_two_hop_over_cold_direct_chain():
    g = Graph()
    g.add(I("me", "warm")); g.add(I("warm", "t"))
    g.add(I("me", "cold", "email", date(2023, 1, 1), False)); g.add(I("cold", "t"))
    path, w = g.warmest_path("me", "t", T)
    assert path == ["me", "warm", "t"] and w > 0

def test_max_hops():
    g = Graph()
    for a, b in [("me", "a"), ("a", "b"), ("b", "c"), ("c", "t")]:
        g.add(I(a, b))
    assert g.warmest_path("me", "t", T, max_hops=3)[0] is None
    assert g.warmest_path("me", "t", T, max_hops=4)[0] is not None

def test_unknown_person():
    assert Graph().warmest_path("me", "x", T) == (None, 0.0)

def test_no_cycles():
    g = Graph()
    g.add(I("me", "a")); g.add(I("a", "b")); g.add(I("b", "a")); g.add(I("b", "t"))
    path, _ = g.warmest_path("me", "t", T)
    assert len(path) == len(set(path))

def test_intro_text():
    assert "Ask alex" in intro_ask(["me", "alex", "dana", "t"], 0.5)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in fns:
        f()
    print(f"{len(fns)} passed")
