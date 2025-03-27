from datetime import datetime
from enum import IntEnum

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserPerssion(IntEnum):
    SuperAdministrator = 0
    Administrator = 1
    Guest = 2


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, comment="用户名")
    password: Mapped[str] = mapped_column(String(64), comment="密码")

    # 信息
    alias: Mapped[str] = mapped_column(String(50), nullable=True, comment="姓名")
    email: Mapped[str] = mapped_column(String(50), nullable=True, comment="邮箱")
    phone: Mapped[str] = mapped_column(String(11), nullable=True, index=True, comment="手机")
    wechat: Mapped[str] = mapped_column(String(50), nullable=True, comment="微信")

    # 状态
    permssion: Mapped[UserPerssion] = mapped_column(Integer, default=False, index=True, comment="权限等级")

    # 事件
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    login_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="登录时间")
    
    # delete_flag

