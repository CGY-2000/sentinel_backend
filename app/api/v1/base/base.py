import json

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException

router = APIRouter()
SECRET_KEY = "3488a63e1765035d386f05409663f55c83bfae3b3c61a932744b20ad14244dcf"
ALGORITHM = "HS256"


async def test(token: str = Header(alias='Authorization')):
    print(token)
    if not token:
        raise HTTPException(status_code=400, detail="token is empty")


@router.post("/test", summary="获取token", dependencies=[Depends(test)])
async def login_access_token(
):
    return {"code": 0, "token": '11'}
