import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent
from models import Expression, CalculatorLog   # <-- import Pydantic models

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
def calculate(expression: Expression):   # <-- use Expression model
    try:
        code = expression.expand_percent_expr()
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expression.expr, "result": "", "error": msg}

        log = CalculatorLog(
            timestamp=datetime.now(),
            expr=expression.expr,
            result=result,
        )
        history.appendleft(log.dict())   # store as dict for serialization

        return {"ok": True, "expr": expression.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expression.expr, "error": str(e)}


@app.get("/history", response_model=list[CalculatorLog])   # <-- enforce response model
def get_history(limit: int = 50):
    return list(history)[: max(0, min(limit, HISTORY_MAX))]


@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True, "cleared": True}