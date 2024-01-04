from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from piro_api.exceptions import ValidationError
from piro_api.models import AppGenericException, MessageResponse
from piro_api.settings import Settings, get_settings


def create_app():
    app = FastAPI()

    # cors middleware
    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/prueba")
    async def get_test_message():
        return {'message': "This is prueba"}
    
    @app.get("/api/test/message")
    async def get_test_message():
        return {'message': "Test message"}

    @app.get("/api/version")
    async def get_test_message(config: Settings = Depends(get_settings)):
        return {'version': config.version}

    from .modules.catalogs import product as catalog_product
    from .modules.catalogs import category as category
    from .modules.catalogs import ventas as ventas
    from .modules.catalogs import Reportes as reportes

    app.include_router(catalog_product.router, tags=['catalog_product'])
    app.include_router(category.router, tags=['category'])
    app.include_router(ventas.router, tags=['ventas'])
    app.include_router(reportes.router, tags=['Reportes'] )


    @app.exception_handler(AppGenericException)
    async def app_generic_exception_handler(request: Request, exc: AppGenericException):
        return JSONResponse(
            status_code=exc.http_response_status_code,
            content=MessageResponse(code=exc.code, message=exc.message).dict(),
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=exc.status_code,
            content=MessageResponse(code=0, message=exc.message).dict(),
        )

    return app
