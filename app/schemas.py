from pydantic import BaseModel
from datetime import datetime


class BaseExpression(BaseModel):
    expr: str


class ExpressionIn(BaseExpression):
    """Input model for calculator expression."""
    pass


class ExpressionOut(BaseExpression):
    """Output log that extends the input expression."""
    timestamp: datetime
    result: float
