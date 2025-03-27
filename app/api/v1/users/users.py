import jwt
from fastapi import APIRouter, Depends

from app.core.dependency import judge_authed, judge_permission
from app.databse.curds import users as curd_users
from app.schemas import Response
from app.schemas import users as schema_users
from configure import Settintg

router = APIRouter()


@router.post("/create", summary="创建用户", dependencies=[Depends(judge_permission)])
async def user_craete(
    user: schema_users.User = Depends(curd_users.user_create, use_cache=False)
):
    return Response(data=user)


@router.get("/query", summary="用户查询")
async def user_query(users: list[schema_users.User] = Depends(curd_users.user_query)):
    return Response(data=users)


@router.get(
    "/delete",
    summary="删除用户",
    dependencies=[Depends(judge_permission), Depends(curd_users.user_delete)],
)
async def user_delete():
    return Response()


@router.post("/update", summary="更新用户", dependencies=[Depends(judge_permission)])
async def user_update(user: schema_users.User = Depends(curd_users.user_update)):
    return Response(data=user)


@router.post("/login", summary="登录")
async def user_login(user: schema_users.User = Depends(curd_users.user_login)):
    return Response(data=user)


@router.post("/access_token", summary="获取token")
async def user_access_token(user: schema_users.User = Depends(curd_users.user_login)):
    jwt_user = schema_users.JwtUser(
        id=user.id,
        username=user.username,
        permssion=user.permssion,
        exp=user.login_at + Settintg.JWT_EXPIRE_TIME,
    )
    token = jwt.encode(
        jwt_user.model_dump(), Settintg.JWT_SECRET_KEY, algorithm=Settintg.JWT_ALGORITHM
    )
    return Response(data=token)
