# warm-path

A small, local Python demo that ranks introduction paths using a relationship graph. Given a CSV of sample interactions, it scores connections by recency and reciprocity, finds a path to each target, and drafts an ask to the first connector.

## Quick start

Python 3.9 or later. No external dependencies.

```bash
python3 -m warm_path examples/sample.csv --me me --to vp_sales cro --today 2026-10-14
```

The included CSV is synthetic example data, not a real contact history. The command prints ranked paths and suggested introduction asks. It does not connect to email or calendar, and does not send messages.

## How scoring works

- Interaction kinds have different weights. Older interactions lose half their weight every 365 days.
- One-way interactions count 40% as much as two-way interactions.
- Tie strength is `1 - exp(-total weight)`, with diminishing returns from more history.
- Path warmth is the product of tie strengths, with a 15% penalty per additional intermediary.
- The search uses negative log costs and allows up to 3 hops by default.

These are simple demo heuristics, not measured probabilities of an introduction succeeding.

## Tests

Run the standard-library test suite from the repository root:

```bash
PYTHONPATH=. python3 tests/test_graph.py
```

## Limits and next steps

This prototype only reads a local CSV. It has no automatic identity resolution, account-fit model or live email/calendar imports. Treat real interaction histories as private data. The suggested asks are drafts for a person to review, not messages ready to send automatically.
