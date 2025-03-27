from contextlib import asynccontextmanager
from datetime import datetime
from hashlib import sha256
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy import and_, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.databse.common import get_session
from app.databse.models import users
from app.schemas import users as schema_users


async def user_create(
    create_data:schema_users.UserCreate, session: AsyncSession = Depends(get_session)
):
    if create_data.permssion == users.UserPerssion.SuperAdministrator:
        raise HTTPException(status_code=400, detail="禁止创建超级管理员")
    sql = select(users.User).where(users.User.username == create_data.username)
    query = await session.execute(sql)
    if query.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="用户名已存在")
    model = users.User(**create_data.model_dump())
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return schema_users.User.model_validate(model)


async def user_query(
    username: Optional[str] = None, 
    alias: Optional[str] = None, 
    permission: Optional[users.UserPerssion] = None, 
    session: AsyncSession = Depends(get_session),
) -> list[schema_users.User]:
    sql = select(users.User)
    if permission is not None:
        sql = sql.where(users.User.permssion == permission)
    if username:
        sql = sql.where(users.User.username.like(f"%{username}%"))
    if alias:
        sql = sql.where(users.User.alias.like(f"%{alias}%"))
    query = await session.execute(sql)
    results = query.scalars()
    return [schema_users.User.model_validate(result) for result in results]


async def user_delete(
    username: Optional[str] = None,
    id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
):
    if not username and not id:
        # 参数错误
        raise HTTPException(status_code=400, detail="参数错误")
    if id == 0 or username == 'admin':
        # 禁止删除超级管理员
        raise HTTPException(status_code=400, detail="禁止删除超级管理员")
    sql = select(users.User)
    if username:
        sql = sql.where(users.User.username == username)
    if id:
        sql = sql.where(users.User.id == id)
    query = await session.execute(sql)
    model = query.scalar_one_or_none()
    if model is None:
        raise HTTPException(status_code=400, detail="用户不存在")
    await session.delete(model)
    await session.commit()


async def user_update(
    update_data: schema_users.UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    sql = select(users.User).where(users.User.username == update_data.username)
    query = await session.execute(sql)
    model = query.scalar_one_or_none()
    if model is None:
        raise HTTPException(status_code=400, detail="用户不存在")
    # 更新数据
    model.username = update_data.username
    model.password = update_data.password
    model.alias = update_data.alias
    model.email = update_data.email
    model.phone = update_data.phone
    model.wechat = update_data.wechat
    model.updated_at = datetime.now()
    await session.commit()
    await session.refresh(model)
    return schema_users.User.model_validate(model)

async def user_login(
    login_data: schema_users.UserLogin, session: AsyncSession = Depends(get_session)
) -> schema_users.User:
    # sql = select(users.User).where(users.User.username == login_data.username)
    # 判断用户名密码是否正确，使用count
    sql = select(users.User).where(
        and_(
            users.User.username == login_data.username,
            users.User.password == login_data.password,
        )
    )
    query = await session.execute(sql)
    user = query.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    user.login_at = datetime.now()
    await session.commit()
    await session.refresh(user)
    return schema_users.User.model_validate(user)


async def user_init():
    _get_session = asynccontextmanager(get_session)
    async with _get_session() as session:
        sql = select(func.count(users.User.id))
        result = (await session.execute(sql)).scalar()
        if result != 0:
            return
        hash = sha256('123456789'.encode())
        model = users.User(
            username="Admin",
            password=hash.hexdigest(),
            alias="管理员",
            permssion=users.UserPerssion.SuperAdministrator,
        )
        session.add(model)
        await session.commit()
