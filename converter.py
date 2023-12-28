from moviepy.video.io.VideoFileClip import VideoFileClip
import re, os
import difflib


class Converter:
    def __init__(self, location, title):
        self.title = title
        self.location = location

    def convert(self):
        # Convert the file
        print("Converting file: " + self.title)
        try:
            print("Finding Video")
            clip = VideoFileClip(f"{self.location}/{self.title}.mp4")
            print("Converting to mp3")
            clip.audio.write_audiofile(f"./Downloads/{self.title}.mp3", codec='mp3')
            clip.close()

            return True
        except Exception as e:
            print(e)
            return False
