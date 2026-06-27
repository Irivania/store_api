from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from store.core.config import settings
from store.routers import api_router
from store.core.exceptions import AppException

class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            version="0.0.1",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH
        )
        self.add_exception_handler(AppException, self.app_exception_handler)
        self.add_exception_handler(RequestValidationError, self.validation_exception_handler)

    async def app_exception_handler(self, request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    async def validation_exception_handler(self, request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

app = App()
app.include_router(api_router)
