from dataclasses import dataclass
from datetime import timedelta


@dataclass
class Settintg:
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_TIME: timedelta = timedelta(minutes=15)
