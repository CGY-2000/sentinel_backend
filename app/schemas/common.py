from typing import Any, Optional

from pydantic import BaseModel, NonNegativeInt


class Response(BaseModel):
    code: NonNegativeInt = 0
    msg: str = 'success'
    data: Optional[Any] = None