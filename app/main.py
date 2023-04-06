from fastapi import FastAPI

from app.db.base import get_session
from app.exceptions.handlers import validation_exception_handler, exception_handler
from fastapi.exceptions import RequestValidationError

from app.routers.auth import router


class Api4ID(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.get_db_session = get_session

docs_url = "/api/docs"
app =Api4ID( docs_url=docs_url)
app.include_router(router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, exception_handler)
