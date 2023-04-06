from http import HTTPStatus

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils import response_message


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    response_content = response_message()
    response_content["success"] = False
    response_content["data"] = {
        "message": "Errors occurred during validation",
        "detail": exc.errors(),
    }

    return JSONResponse(response_content, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)


async def exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    response_content = response_message()
    response_content["success"] = False
    response_content["data"] = {"message": str(exc), "detail": {}}

    status_code = (
        exc.status_code
        if hasattr(exc, "status_code")
        else HTTPStatus.INTERNAL_SERVER_ERROR
    )

    return JSONResponse(response_content, status_code=status_code)
