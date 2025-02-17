import logging
import traceback
from typing import Final

import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger: Final = logging.getLogger("middleware")
access_logger: Final = structlog.stdlib.get_logger("api.access")

class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        # TODO: Handle EndOfStream exception
        except Exception as e:
            stack_trace = traceback.format_exception(type(e), e, e.__traceback__)
            logger.error(f"Uncaught exception: {e}", stack_info=True, exc_info=True)
            return JSONResponse(status_code=500, content={"detail": f"Internal server error: {e}", "stack": stack_trace})

