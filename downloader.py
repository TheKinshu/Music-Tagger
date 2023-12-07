import time
import os
from pytube import YouTube, Playlist
from threading import Thread
from converter import Converter
import logging


# Download youtube video
class downloader:
    def __init__(self, url, path, resolution, logger=None, test=None, window=None):
        self.window = window
        self.url = url
        self.path = path
        self.resolution = resolution
        self.logger = logger
        self.test = test
        self.title = None
        self.playlist = None
        self.regex = ['/', '\\', '?', '<', '>', '?', '*', '"', '|', ':', '.', ',', "'", '#', '$', ';']

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
                try:
                    for i in self.regex:
                        if i in self.title:
                            self.title = self.title.replace(i, "")
                    self.logger.info("Converting file: " + self.title)
                except Exception as e:
                    self.logger.error("Error converting file: " + str(e))

                Converter("./Video", self.title).convert()
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
            Thread(target=self.found.download, kwargs={"output_path": self.path}).start()
            self.logger.info("Download Complete")

            self.test = True
            return True
        except Exception as e:
            self.logger.error("Error downloading video:" + str(e))
            self.test = True
            return False

    def download_video(self, video_url, index, total_videos):
        try:
            self.video = YouTube(video_url)
            self.title = self.video.title

            self.window.update_idletasks()
            self.video.streams.filter(progressive=True, file_extension='mp4', resolution=self.resolution).order_by(
                'resolution').desc().first().download(output_path=self.path)

            # convert to mp3
            self.logger.info("Converting to mp3")

            try:
                for i in self.regex:
                    if i in self.title:
                        self.title = self.title.replace(i, "")
                self.logger.info("Converting file: " + self.title)
                Converter("./Video", self.title).convert()
            except Exception as e:
                self.logger.error("Error converting file: " + str(e))


        except Exception as e:
            self.logger.error("Error downloading video:" + str(e))
            return False

    def download_async(self, url):
        try:
            playlist = Playlist(url)
            total_videos = len(playlist.video_urls)

            for index, video_url in enumerate(playlist.video_urls, start=1):
                self.download_video(video_url, index, total_videos)
            pass
        except Exception as e:
            self.logger.error("Error downloading video:" + str(e))

    def playlist_download(self):
        try:
            self.logger.info("Finding Videos")
            download_thread = Thread(target=self.download_async, args=(self.url,))
            download_thread.start()
        except Exception as e:
            self.logger.error("Error downloading video:" + str(e))
            return False


# downloader("https://www.youtube.com/watch?v=GQrppVgwz5o", "Downloads", "720p", logging.getLogger()).single_download()
# Download file from url
def get_test():
    return None
