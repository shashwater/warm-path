# warm-path

Find the warmest intro path from you to a target person, given your interaction history.

Cold outreach converts worse than a warm intro. This tool builds a relationship graph from
interaction logs (meetings, calls, emails, coworker overlap), scores each tie by recency and
reciprocity, and finds the path with the highest combined warmth. It then writes the ask you would
send to the first connector.

## How it scores

- Each interaction adds weight by kind (meeting > call > email > message), halved every 365 days.
- One-way interactions count 40% as much as two-way ones.
- Tie strength = `1 - exp(-total weight)`, so more history helps with diminishing returns.
- Path warmth = product of tie strengths, with a 15% penalty per extra intermediary.
- Search is Dijkstra on `-log(strength)`, capped at 3 hops by default.

## Use

```
python3 -m warm_path examples/sample.csv --me me --to vp_sales cro --today 2026-10-14
```

CSV columns: `a,b,kind,date,two_way`. No dependencies beyond Python 3.9+.

## Test

```
PYTHONPATH=. python3 tests/test_graph.py
```

## Next

Pull interactions straight from email and calendar, and rank targets by account fit.
