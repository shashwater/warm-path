"""Turn a path into a forwardable intro request for the first connector."""


def intro_ask(path, warmth, goal="a quick chat"):
    if not path or len(path) < 3:
        return "Direct connection exists; no intro needed." if path else "No path found."
    me, connector, *rest = path
    target = path[-1]
    hops = " -> ".join(path)
    return (
        f"Path: {hops} (warmth {warmth:.2f})\n"
        f"Ask {connector}: \"Would you be open to introducing me to {target}"
        f"{' via ' + ', '.join(rest[:-1]) if len(rest) > 1 else ''} for {goal}? "
        f"Happy to send a 3-line blurb you can forward.\""
    )
