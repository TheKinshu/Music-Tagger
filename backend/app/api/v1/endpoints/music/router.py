import asyncio
from typing import Final

from fastapi import APIRouter, Depends
from starlette.requests import Request
from structlog import get_logger

from backend.app.api.v1.endpoints.music.models import DownloadBody
from backend.app.common.controller import download_video, download_mp3
from backend.app.common.dependencies import get_ws_manager
from backend.app.common.models import ErrorResponseModel, CommonResponse
from backend.app.intergration.websocket import WSManager

logger: Final = get_logger()

router = APIRouter(responses={403: {"model": ErrorResponseModel},
                              401: {"model": ErrorResponseModel},
                              400: {"model": ErrorResponseModel},
                              404: {"model": ErrorResponseModel}},
                   dependencies=[])

from pytube import YouTube

@router.post("/single-download", operation_id="SingleDownload")
async def single_download(request: Request, body: DownloadBody, ws_manager: WSManager = Depends(get_ws_manager)) -> CommonResponse:
    user_id = '854d88ea-d1c4-4144-8f77-79783300023a'
    # active_sessions = request.app.state.active_sessions
    url = body.url
    output_path = body.output_path
    resolution = body.resolution
    asyncio.create_task(download_mp3(url=url,
                                       path=output_path,
                                       resolution=resolution,
                                       noPlaylist=True,
                                       ws_manager=ws_manager,
                                       user_id=user_id))

    return CommonResponse(success=True)


@router.post("/playlist-download", operation_id="PlaylistDownload")
async def playlist_download(request: Request, body: DownloadBody, ws_manager: WSManager = Depends(get_ws_manager)) -> CommonResponse:
    user_id = '854d88ea-d1c4-4144-8f77-79783300023a'

    url = body.url
    output_path = body.output_path
    resolution = body.resolution
    asyncio.create_task(download_mp3(url=url,
                                       path=output_path,
                                       resolution=resolution,
                                       noPlaylist=False,
                                       ws_manager=ws_manager,
                                       user_id=user_id))
    return CommonResponse(success=True)

@router.post("/single-download-video", operation_id="SingleVideo")
async def single_video_download(request: Request, body: DownloadBody) -> CommonResponse:
    url = body.url
    output_path = body.output_path
    resolution = body.resolution
    asyncio.create_task(download_video(url=url,
                                       path=output_path,
                                       resolution=resolution,
                                       noPlaylist=True))
    return CommonResponse(success=True)

@router.post("/playlist-download-video", operation_id="PlaylistVideo")
async def playlist_video_download(request: Request, body: DownloadBody) -> CommonResponse:
    url = body.url
    output_path = body.output_path
    resolution = body.resolution
    asyncio.create_task(download_video(url=url,
                                       path=output_path,
                                       resolution=resolution,
                                       noPlaylist=False))
    return CommonResponse(success=True)

