from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
    ResponseValidationError,
)
from fastapi.requests import Request
from fastapi.responses import JSONResponse


async def HttpExcHandle(_: Request, exc: HTTPException) -> JSONResponse:
    content = dict(code=exc.status_code, msg=exc.detail, data=None)
    return JSONResponse(content=content, status_code=200)


async def RequestValidationHandle(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    content = dict(code=422, msg=f"RequestValidationError, {exc}")
    print(exc)
    return JSONResponse(content=content, status_code=422)


async def ResponseValidationHandle(
    _: Request, exc: ResponseValidationError
) -> JSONResponse:
    content = dict(code=500, msg=f"ResponseValidationError, {exc}")
    return JSONResponse(content=content, status_code=500)
