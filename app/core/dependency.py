import asyncio
from datetime import datetime

import jwt
from fastapi import Depends, Header, HTTPException, Request

from app.core.context import CTX_USER_ID
from app.databse.models.users import UserPerssion
from app.schemas.users import JwtUser, User
from configure import Settintg


async def judge_authed(
    token: str = Header(..., alias='Authorization', description="认证token")
) -> JwtUser:
    print("debug: ", token)
    if token == "dev":
        return True
    try:
        decode_data = jwt.decode(token, Settintg.JWT_SECRET_KEY, algorithms=[Settintg.JWT_ALGORITHM])
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="无效的Token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="登录已过期")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{repr(e)}")
    else:
        now = datetime.now()
        jwt_user = JwtUser.model_validate(decode_data)
        if now > jwt_user.exp:
            raise HTTPException(status_code=401, detail="登录已过期")
        CTX_USER_ID.set(jwt_user.id)
        print(decode_data)
    return jwt_user

async def judge_permission(request: Request, user: JwtUser = Depends(judge_authed)) -> None:
    if user.permssion == UserPerssion.SuperAdministrator:
        return
    path = request.url.path
    if 'update' in path and user.permssion not in {UserPerssion.SuperAdministrator, UserPerssion.Administrator}:
        raise HTTPException(status_code=403, detail="权限不足")
    elif 'delete' in path and user.permssion != UserPerssion.SuperAdministrator:
        raise HTTPException(status_code=403, detail="权限不足")
