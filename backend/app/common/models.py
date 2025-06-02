from enum import Enum
from typing import Optional, Union, Literal

from pydantic import BaseModel, ConfigDict
from structlog import get_logger

logger = get_logger()

class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class ErrorEnum(str, Enum):
    forbidden = 'forbidden'
    bad_request = 'bad-request'
    unprocessable_entity = 'unprocessable-entity'
    unauthorized = 'unauthorized'
    server_error = 'server-error'
    not_found = 'not-found'
    unknown_error = 'unknown-error'

class ErrorResponseModel(StrictBaseModel):
    detail: str
    error: ErrorEnum

class CommonResponse(StrictBaseModel):
    success: bool

class WSMessagePayloadLog(StrictBaseModel):
    message: str


class WSMessagePayloadDownload(StrictBaseModel):
    link: str
    file_name: str
    script_name: str
    created_at: float


class WSMessagePayloadProcess(StrictBaseModel):
    is_running: bool
    script_name: Optional[str] = None


class WSMessage(StrictBaseModel):
    message_payload: Union[WSMessagePayloadLog, WSMessagePayloadDownload, WSMessagePayloadProcess]
    message_type: Literal['info', 'error', 'log', 'link', 'process'] = 'log'

class HealthStatus(StrictBaseModel):
    status: bool


class YTDLPLogger:
    def debug(self, msg):
        logger.debug(msg)
    def warning(self, msg):
        logger.warning(msg)
    def error(self, msg):
        logger.error(msg)
