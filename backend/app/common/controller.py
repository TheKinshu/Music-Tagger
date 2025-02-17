from pytube import YouTube
from structlog import get_logger

logger = get_logger()

async def download_video(url, path, resolution):
    try:
        video = YouTube(url)
        title =  video.title
        streams =  video.streams
        video = streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        video.download(output_path=path)
        # await video.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).order_by(
        #     'resolution').desc().first().download(output_path=path)
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        return False
    return True