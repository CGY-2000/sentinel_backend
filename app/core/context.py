from contextvars import ContextVar

CTX_USER_ID: ContextVar[int] = ContextVar("user_id", default=0)
