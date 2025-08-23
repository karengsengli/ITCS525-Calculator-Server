from pydantic import BaseModel
from datetime import datetime
from calculator import expand_percent
import re

class Expression(BaseModel):
    expr: str

    def expand_percent_expr(self) -> str:
        """Return the expression after expanding % symbols."""
        return expand_percent(self.expr)


class CalculatorLog(BaseModel):
    timestamp: datetime
    expr: str
    result: float
