import asyncio
import os
import signal

from contextlib import asynccontextmanager
from typing import Final

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse
from structlog import get_logger

from backend.app.api.v1.endpoints.music.router import router as music_router
from backend.app.common.models import ErrorEnum, ErrorResponseModel, HealthStatus, WSMessage, WSMessagePayloadLog, \
    WSMessagePayloadDownload, WSMessagePayloadProcess

from backend.app.intergration.websocket import WSManager
from backend.app.middleware import ErrorMiddleware

logger: Final = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting coroutines in dedicated threads")
    app.state.ws_manager = WSManager()
    app.state.active_sessions = {}
    try:
        yield
    finally:
        logger.info("Received graceful shutdown signal")
        active_sessions = app.state.active_sessions
        for user_id, session in active_sessions.items():
            process = session.get("process")
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                os.kill(process.pid, signal.SIGKILL)
        active_sessions.clear()


app = FastAPI(lifespan=lifespan, description="Toolbox Saas API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "HEAD", "OPTIONS"],
    allow_headers=["X-Requested-With", "Content-Type", "Cache-Control", "Origin", "Accept", "Authorization",
                   "X-Correlation-Id", "X-Service-Origin", "X-Company-Id", "traceparent"],
)

app.add_middleware(ErrorMiddleware)
app.add_middleware(CorrelationIdMiddleware, header_name="X-Correlation-Id")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    error = ErrorEnum.unknown_error
    if exc.status_code == 500:
        error = ErrorEnum.server_error
        logger.error("Internal server error", exc_info=exc.detail)
    elif exc.status_code == 401:
        error = ErrorEnum.unauthorized
        logger.error("Unauthorized", exc_info=exc.detail)
    elif exc.status_code == 403:
        error = ErrorEnum.forbidden
        logger.error("Forbidden", exc_info=exc.detail)
    elif exc.status_code == 404:
        error = ErrorEnum.not_found
        logger.error("Not Found", exc_info=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, "error": error})


@app.get("/")
async def redirect_to_swagger():
    return RedirectResponse(url="/docs")


@app.get("/health", responses={
    403: {"model": ErrorResponseModel},
    401: {"model": ErrorResponseModel},
    400: {"model": ErrorResponseModel},
    404: {"model": ErrorResponseModel}
})
async def health_check() -> HealthStatus:
    return HealthStatus(status=True)

@app.websocket("/ws/console/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint to stream script output to the client.
    """
    await websocket.accept()
    await websocket.app.state.ws_manager.connect(websocket, user_id)
    try:
        logger.info(f"WebSocket connection established for user {user_id}")
        active_sessions = websocket.app.state.active_sessions

        logger.info(f"Active sessions: {active_sessions}")
        if user_id in active_sessions:
            await websocket.app.state.ws_manager.send_process_status(user_id, True,
                                                                     active_sessions[user_id].get("script_name"))
        else:
            await websocket.app.state.ws_manager.send_process_status(user_id, False)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.warning("WebSocket connection closed")
        websocket.app.state.ws_manager.disconnect(websocket, user_id)
    except Exception as e:
        await websocket.app.state.ws_manager.send_log(user_id, f'[error]: {str(e)}')

app.include_router(music_router, prefix="/api/v1/toolbox", tags=["toolbox"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Music Tagger API",
        version="1.0.0",
        summary="Backend api schema for chatbot saas application",
        description="Built with **OpenAPI** 3.0",
        routes=app.routes,
    )
    openapi_schema["components"]["schemas"]["WSMessagePayloadLog"] = WSMessagePayloadLog.model_json_schema()
    openapi_schema["components"]["schemas"]["WSMessagePayloadDownload"] = WSMessagePayloadDownload.model_json_schema()
    openapi_schema["components"]["schemas"]["WSMessagePayloadProcess"] = WSMessagePayloadProcess.model_json_schema()
    openapi_schema["components"]["schemas"]["WSMessage"] = WSMessage.model_json_schema(
        ref_template="#/components/schemas/{model}")
    return openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
