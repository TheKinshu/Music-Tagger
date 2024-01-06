import time
import os
from pytube import YouTube, Playlist
from threading import Thread
from converter import Converter
import logging


def show_progress_bar(s, chunk, bytes_remaining, logger):
    download_percent = int((s.filesize - bytes_remaining) / s.filesize * 100)
    logger.info(f'\rCurrent Download Progress: {download_percent} %')


# Download youtube video
class downloader:
    def __init__(self, url, path, resolution, logger=None, currentDownload=None, window=None):
        self.window = window
        self.url = url
        self.path = path
        self.resolution = resolution
        self.logger = logger
        self.currentDownload = currentDownload
        self.title = None
        self.playlist = None
        self.regex = ['/', '\\', '?', '<', '>', '?', '*', '"', '|', ':', '.', ',', "'", '#', '$', ';']

    def single_download(self):
        try:
            download_thread = Thread(target=self.download_video, args=(self.url, 1, 1))
            download_thread.start()
        except Exception as e:
            self.logger.error("Error downloading video:" + str(e))

    def download_video(self, video_url, index, total_videos):
        try:

            self.video = YouTube(video_url)
            self.title = self.video.title

            self.video.register_on_progress_callback(
                lambda s, chunk, bytes_remaining: show_progress_bar(s, chunk, bytes_remaining, self.logger))

            self.window.update_idletasks()

            self.video.streams.filter(progressive=True, file_extension='mp4', resolution=self.resolution).order_by(
                'resolution').desc().first().download(output_path=self.path)

            # convert to mp3
            self.logger.info("Converting to mp3")

            try:
                for i in self.regex:
                    if i in self.title:
                        self.title = self.title.replace(i, "")
                self.currentDownload(self.title, round(index-1 / total_videos, 2), False)

                Converter("./Video", self.title, self.logger).convert()
                self.currentDownload(self.title, round(index / total_videos, 2), True)

            except Exception as e:
                self.logger.error("Error converting file: " + str(e))

        except Exception as e:
            errorMessage = "Error downloading video:" + str(e) + "\nAttempted to download: " + self.title + "\nLink: " + video_url
            self.logger.error(errorMessage)
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
