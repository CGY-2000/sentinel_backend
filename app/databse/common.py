
from dataclasses import dataclass
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models.base import Base


@dataclass
class DbSetting:
    host: str = "192.168.1.53"
    port: int = 3306
    user: str = "root"
    password: str = "Powerhaven2012"
    database: str = "test_zsx"
    
    @classmethod
    def create_url(cls) -> str:
        """连接地址"""
        return f"mysql+aiomysql://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.database}"


# MySQL 会在连接上未检测到活动 8 小时后自动断开连接
_engine = None
_async_session = None


async def db_init():
    global _engine, _async_session
    _engine = create_async_engine(
        DbSetting.create_url(), pool_recycle=3600
    )
    _async_session = async_sessionmaker(_engine, autoflush=True, expire_on_commit=True)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def de_deinit():
    global _engine
    await _engine.dispose()
    _engine = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    global _async_session
    async with _async_session() as session:
        try:
            yield session
        finally:
            pass


# async def check_db_init():
#     #   import aiomysql
#     import pymysql

#     with pymysql.connect(
#         host=DbSetting.host, 
#         user='root',
#         password='Powerhaven2012',
#         port=DbSetting.port,
#     ) as conn:
#         with conn.cursor() as cur:
#             sql = f"CREATE DATABASE IF NOT EXISTS {DbSetting.database};"
#             cur.execute(sql)
#             conn.commit()
            
#             sql = f"SELECT COUNT(*) FROM mysql.user WHERE user=%s;"
#             result = cur.execute(sql, (DbSetting.user,))
#             print(result)

#             # 查询用户主机
#             sql = f"SELECT * FROM mysql.user WHERE user=%s;"
#             result = cur.execute(sql, (DbSetting.user,))
#             print(result)


#             # sql = "GRANT ALL ON test_zoulee24_test.* to %s;"
#             # result = cur.execute(sql, (DbSetting.user))
#             # print(result)

#             # sql = "GRANT ALL PRIVILEGES ON test_zoulee24.* TO %s@%% IDENTIFIED WITH BY %s"
#             # print(sql % (DbSetting.user, DbSetting.password))
#             # result = cur.execute(sql, (DbSetting.user, DbSetting.password,))
#             # print(result)
# #     # 检查数据库是否存在
# #     async with aiomysql.connect(
# #         host=DbSetting.host, 
# #         user='root',
# #         password='Powerhaven2012',
# #         port=DbSetting.port,
# #         echo=True
# #     ) as conn:
# #         # async with conn.cursor() as cur:
# #         cur = await conn.cursor()
# #         # # 判断数据库是否存在
# #         # sql = f"CREATE DATABASE IF NOT EXISTS {DbSetting.database};"
# #         # await cur.execute(sql)
# #         # # 查询用户是否存在
# #         # sql = f"SELECT COUNT(*) FROM mysql.user WHERE user=%s;"
# #         # result = await cur.execute(sql, (DbSetting.user,))
# #         # print(result)
# #         # if result == 0:
# #         #     pass
# #         # await conn.commit()
        
# #         # 授权数据库
# #         sql = "GRANT ALL PRIVILEGES ON test_zoulee24.* TO %s@'%%' IDENTIFIED BY %s;"
# #         sql = sql % (DbSetting.user, DbSetting.password)
# #         print(sql)
# #         await cur.execute(sql)
# #         await conn.commit()
# #         await cur.close()
