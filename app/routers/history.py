from fastapi import APIRouter, Depends
from app.schemas import ExpressionOut
from app.dependencies import get_history, HISTORY_MAX

router = APIRouter()


@router.get("/history", response_model=list[ExpressionOut])
def read_history(limit: int = 50, history=Depends(get_history)):
    return list(history)[: max(0, min(limit, HISTORY_MAX))]


@router.delete("/history")
def clear_history(history=Depends(get_history)):
    history.clear()
    return {"ok": True, "cleared": True}
