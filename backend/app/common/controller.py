from structlog import get_logger
from yt_dlp import YoutubeDL

from backend.app.common.models import YTDLPLogger
from backend.app.intergration.websocket import WSManager

logger = get_logger()


async def download_mp3(url: str,
                       path: str,
                       resolution: str,
                       user_id: str,
                       ws_manager: WSManager,
                       noPlaylist: bool = True):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './downloads' + '/%(title)s.%(ext)s',
            'extractaudio': True,
            'audioformat': "mp3",
            'noplaylist': noPlaylist,
            'quiet': True,
            # 'progress_hooks': [hook],
            'logger': YTDLPLogger(),  # Custom logger to capture yt_dlp logs

            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ignoreerrors': True,  # Ignore errors like removed videos
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                await ws_manager.send_log(user_id, f"Downloading {url}")
                ydl.download([url])
            except Exception as e:
                logger.error(f"Error downloading music video from: {str(e)}")

    except Exception as e:
        logger.error(f"Error downloading music: {str(e)}")



async def download_video(url, path='./downloads/videos', resolution=None, noPlaylist=True, progress_callback=None):
    try:
        def hook(d):
            if d['status'] == 'downloading':
                progress_data = {
                    'filename': d.get('filename'),
                    'downloaded_bytes': d.get('downloaded_bytes'),
                    'total_bytes': d.get('total_bytes'),
                    'speed': d.get('speed'),
                    'eta': d.get('eta'),
                    'progress': d.get('_percent_str'),
                }
                logger.info("Downloading...", **progress_data)
                if progress_callback:
                    # Send progress to the callback (e.g., WebSocket)
                    import asyncio
                    asyncio.create_task(progress_callback(progress_data))

            elif d['status'] == 'finished':
                logger.info("Download finished", filename=d.get('filename'))
                if progress_callback:
                    import asyncio
                    asyncio.create_task(progress_callback({'status': 'finished', 'filename': d.get('filename')}))

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'noplaylist': noPlaylist,
            'merge_output_format': 'mp4',
            # 'progress_hooks': [hook],
            'quiet': True,  # Prevent default logging to stdout
            'logger': YTDLPLogger(),  # Custom logger to capture yt_dlp logs
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            logger.error("Error in downloading video: ", error=str(e))

    except Exception as e:
        logger.error("Error downloading video", error=str(e))
        return False

    return True
