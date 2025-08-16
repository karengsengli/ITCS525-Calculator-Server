import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter
from typing import Optional

from calculator import expand_percent

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr: str):
    try:
        code = expand_percent(expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}
        # TODO: Add history
        history.append({"expr": expr, "result": result})

        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}

# GET /history?limit=10
@app.get("/history")
def get_history(limit: Optional[int] = Query(None, description="Limit number of history records (0 = all)")):
    if limit is not None and limit > 0:
        return list(history)[-limit:]  # convert deque to list for slicing
    return list(history)

# DELETE /history
@app.delete("/history")
def delete_history():
    history.clear()
    return {"ok": True, "message": "History cleared"}

