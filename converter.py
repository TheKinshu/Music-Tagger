from moviepy.video.io.VideoFileClip import VideoFileClip

class Converter:
    def __init__(self, path):
        self.path = path

    def convert(self):
        # Convert the file
        print("Converting file: " + self.path)
        try:
            title = self.path.split(".")[0].split("/")[-1]
            print("Finding Video")
            clip = VideoFileClip(self.path)
            print("Converting to mp3")
            clip.audio.write_audiofile(f"./Downloads/{title}.mp3", codec='mp3')
            clip.close()

            return True
        except Exception as e:
            print(e)
            return False
