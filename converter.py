from moviepy.video.io.VideoFileClip import VideoFileClip
import re, os
import difflib

class Converter:
    def __init__(self, title):
        self.title = title
        self.regex = ['/', '\\', '?', '<', '>', '?', '*', '"', '|', ':', '.', ',', "'", '#', '$', ';']

    def convert(self):
        # Convert the file
        print("Converting file: " + self.title)
        try:
            for i in self.regex:
                if i in self.title:
                    self.title = self.title.replace(i, "")

            print("Finding Video")
            clip = VideoFileClip(self.title)
            print("Converting to mp3")
            clip.audio.write_audiofile(f"./Downloads/{self.title}.mp3", codec='mp3')
            clip.close()

            return True
        except Exception as e:
            print(e)
            return False

    def converttest(self):
        # Convert the file
        print("Converting file: " + self.title)
        try:

            best_match, similarity = difflib.get_close_matches("Moonthief / キタニタツヤ - Moonthief / Tatsuya Kitani", ["Moonthief / キタニタツヤ - Moonthief / Tatsuya Kitani"], n=1, cutoff=0.6)[0]

            print(best_match)


            return True
        except Exception as e:
            print(e)
            return False

# 'Video/MEGAVERSE.mp4'
# Video/Moonthief  キタニタツヤ - Moonthief  Tatsuya Kitani.mp4
# Video/Moonthief / キタニタツヤ - Moonthief / Tatsuya Kitani.mp4
Converter('Moonthief / キタニタツヤ - Moonthief / Tatsuya Kitani').convert()
