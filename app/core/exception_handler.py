from fastapi import Request, status
from app.utils.response import error_response
from app.core.exception import BaseAppException

def register_exception_handlers(app):

    @app.exception_handler(BaseAppException)
    async def base_exception_handler(request: Request, exc: BaseAppException):
        return error_response(
            message=exc.message,
            status_code=exc.status_code
        )

    @app.exception_handler(Exception)
    async def global_exception(request: Request, exc: Exception):
        print("UNHANDLED ERROR:", exc)
        import traceback
        traceback.print_exc()
        raise

    return error_response(
            message="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )