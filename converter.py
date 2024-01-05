import logging
import re, os
os.environ["IMAGEIO_FFMPEG_EXE"] = "./ffmpeg.exe"
from moviepy.video.io.VideoFileClip import VideoFileClip

class Converter:
    def __init__(self, location, title, logger):
        self.title = title
        self.location = location
        self.logger = None
    def convert(self):
        # Convert the file
        logging.info("Converting file: " + self.title)
        try:
            logging.info("Finding Video")
            # Find the video
            if os.path.isfile(f"{self.location}/{self.title}.mp4"):
                logging.info("Found Video")

            location = f"{self.location}/{self.title}.mp4"
            clip = VideoFileClip(location)
            logging.info("Converting to mp3")
            clip.audio.write_audiofile(f"./Downloads/{self.title}.mp3", codec='mp3')
            clip.close()

            return True
        except Exception as e:
            logging.error(e)
            return False
