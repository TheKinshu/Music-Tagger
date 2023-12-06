import time
import os
from pytube import YouTube
import threading
from converter import Converter
import logging


# Download youtube video
class downloader:
    def __init__(self, url, path, resolution, logger=None, test=None):
        self.url = url
        self.path = path
        self.resolution = resolution
        self.logger = logger
        self.test = test

    def on_progress(self, stream, chunk, bytes_remaining):
        try:
            """Callback function"""
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            pct_completed = bytes_downloaded / total_size * 100
            self.logger.info(f"{pct_completed:.2f}% downloaded")

            if round(pct_completed, 2) == 100.0:
                time.sleep(2)
                self.logger.info("Download Complete")
                self.logger.info("Converting to mp3")
                Converter(f"{self.path}/{self.title}.mp4").convert()
                self.logger.info("Conversion Complete")

        except Exception as e:
            print(e)

    def get_test(self):
        return self.test

    def single_download(self):
        try:
            self.logger.info("Finding Video")
            self.logger.info("video url: " + self.url)
            self.video = YouTube(self.url)
            self.video.register_on_progress_callback(self.on_progress)
            self.title = self.video.title
            self.logger.info("Downloading Video")
            self.found = (self.video.streams.filter(progressive=True, file_extension='mp4', resolution=self.resolution)
                          .order_by('resolution').desc().first())
            threading.Thread(target=self.found.download, kwargs={"output_path": self.path}).start()
            self.logger.info("Download Complete")

            self.test = True
            return True
        except Exception as e:
            self.logger.error("Error downloading video")
            self.test = True
            return False


# downloader("https://www.youtube.com/watch?v=GQrppVgwz5o", "Downloads", "720p", logging.getLogger()).single_download()
# Download file from url
def get_test():
    return None
