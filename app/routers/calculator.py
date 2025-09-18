import math
from datetime import datetime
from fastapi import APIRouter, Depends
from asteval import Interpreter

from app.schemas import ExpressionIn, ExpressionOut
from app.dependencies import expand_percent, get_history

router = APIRouter()

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@router.post("/calculate")
def calculate(expression: ExpressionIn, history=Depends(get_history)):
    try:
        code = expand_percent(expression.expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expression.expr, "result": "", "error": msg}

        log = ExpressionOut(
            timestamp=datetime.now(),
            expr=expression.expr,
            result=result,
        )
        history.appendleft(log.dict())

        return {"ok": True, "expr": expression.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expression.expr, "error": str(e)}
