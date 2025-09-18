import re
from collections import deque
from fastapi import Depends

_percent_pair = re.compile(r"""
    (?P<a>\d+(?:\.\d+)?)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""", re.VERBOSE)
#_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")

def expand_percent(expr: str) -> str:
    """Handle A op B% and standalone N% patterns."""
    s = expr.replace("×", "*").replace("÷", "/")
    while True:
        # Replace A op B%
        m = _percent_pair.search(s)
        if not m:
            break
        a, op, b = m.group("a", "op", "b")
        if op in "+-":
            repl = f"{a} {op} (({b}/100)*{a})"
        elif op == "*":
            repl = f"{a} * ({b}/100)"
        else:
            repl = f"{a} / ({b}/100)"
        s = s[:m.start()] + repl + s[m.end():]

    # Replace B%
    #s = _number_percent.sub(lambda m: f"({m.group('n')}/100)", s)

    # Replace standalone N% (handle "N%X" as (N/100)*X)
    s = re.sub(r"(\d+(?:\.\d+)?)%(?=\d|\()", r"(\1/100)*", s)
    # Replace simple N%
    s = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1/100)", s)
    return s


# ---- history ----
HISTORY_MAX = 1000
_history = deque(maxlen=HISTORY_MAX)

def get_history():
    return _history
