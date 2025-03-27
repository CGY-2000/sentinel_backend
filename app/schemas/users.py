from datetime import datetime
from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    StringConstraints,
    field_serializer,
    field_validator,
)

from app.databse.models.users import UserPerssion


# 参考 app/databse/models/user.py 写对应的pydantic模型
class UserLogin(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=64)] = Field(exclude=True)


class UserUpdate(UserLogin):
    # 信息
    alias: Optional[Annotated[str, StringConstraints(min_length=3, max_length=50)]] = None
    email: Optional[Annotated[str, StringConstraints(min_length=5, max_length=50)]] = None
    phone: Optional[Annotated[str, StringConstraints(min_length=11, max_length=11)]] = None
    wechat: Optional[Annotated[str, StringConstraints(min_length=8, max_length=50)]] = None


class UserCreate(UserUpdate):
    permssion: UserPerssion


class User(UserCreate):
    model_config = ConfigDict(from_attributes=True)

    id: NonNegativeInt
    # 事件
    created_at: datetime = Field(exclude=True)
    updated_at: datetime = Field(exclude=True)
    login_at: datetime = Field(exclude=True)


class JwtUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: NonNegativeInt
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    permssion: UserPerssion
    exp: datetime

    @field_serializer('exp')
    def serialize_exp(self, exp: datetime) -> int:
        return int(exp.timestamp() * 1000)

    @field_validator('exp', mode='before')
    def validate_exp(cls, exp: datetime | int) -> datetime:
        if isinstance(exp, int):
            print(f"DEBUG:\t{exp=}")
            return datetime.fromtimestamp(exp / 1000)
        elif isinstance(exp, datetime):
            return exp
        else:
            raise ValueError("exp must be int or datetime")

