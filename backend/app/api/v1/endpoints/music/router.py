import asyncio
import os
import signal
from typing import Final, List, Dict, Union, Optional

from fastapi import APIRouter, Depends, Security, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPBearer
from starlette.requests import Request
from structlog import get_logger

from backend.app.api.v1.endpoints.music.models import DownloadBody
from backend.app.common.controller import download_video
from backend.app.common.models import ErrorResponseModel, CommonResponse

logger: Final = get_logger()

router = APIRouter(responses={403: {"model": ErrorResponseModel},
                              401: {"model": ErrorResponseModel},
                              400: {"model": ErrorResponseModel},
                              404: {"model": ErrorResponseModel}},
                   dependencies=[])

from pytube import YouTube

@router.post("/single-download", operation_id="SingleDownload")
async def single_download(request: Request, body: DownloadBody) -> CommonResponse:
    url = body.url
    output_path = body.output_path
    resolution = body.resolution
    asyncio.create_task(download_video(url=url,
                                       path=output_path,
                                       resolution=resolution))

    return CommonResponse(success=True)


@router.post("/playlist-download", operation_id="PlaylistDownload")
async def playlist_download(request: Request, body: DownloadBody) -> CommonResponse:
    url = body.url
    output_path = body.output_path
    resolution = body.resolution
    asyncio.create_task(download_video(url=url,
                                       path=output_path,
                                       resolution=resolution))
    return CommonResponse(success=True)