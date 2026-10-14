import argparse
from datetime import date

from .graph import load_csv
from .intro import intro_ask


def main(argv=None):
    p = argparse.ArgumentParser(prog="warm-path", description="Find the warmest intro path to a target.")
    p.add_argument("csv")
    p.add_argument("--me", required=True)
    p.add_argument("--to", required=True, nargs="+")
    p.add_argument("--max-hops", type=int, default=3)
    p.add_argument("--today", default=date.today().isoformat())
    a = p.parse_args(argv)
    g = load_csv(a.csv)
    rows = g.top_paths(a.me, a.to, date.fromisoformat(a.today), a.max_hops)
    if not rows:
        print("no path found")
        return 1
    for t, path, w in rows:
        print(intro_ask(path, w))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
