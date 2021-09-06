from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from moviepy.editor import *

import requests, os

class Download():
    def __init__(self, URL) -> None:
        self.download_location = "Downloads/"
        self.yt = YouTube(URL)
        self.music_title = ""
        self.thumbnail_url = ""
        self.regex = ['/', '\\', '?', '<', '>', '?', '*', '"', '|', ':', '.', ',']
    
    def download_link(self):
        try:
            print("Finding Video....")

            self.music_title = self.yt.title
            self.thumbnail_url = self.yt.thumbnail_url

            print("Video Found!")

            # Find all the character not allow for file naming

            for i in self.regex:
                if i in self.music_title:
                    print("{} character has been found in the title and is being deleted!".format(i))
                    self.music_title = self.music_title.replace(i, "")

            with open("thumbnail\\{}.jpg".format(self.music_title), 'wb') as handle:
                response = requests.get(self.thumbnail_url, stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)

            print("Downloading Video please wait......")
            
            stream = self.yt.streams.filter(file_extension='mp4').first()
            stream.download(self.download_location)
            
            print("Download complete!")

            # Location of mp4 


            location = "{}{}.mp4".format(self.download_location, self.music_title)

            # Convert video to audio
            print("Converting audio....")
            video = VideoFileClip(location)
            video.audio.write_audiofile("{}/{}.mp3".format(self.download_location, self.music_title))
            video.close()
            print("Convert complete!")

            # Remove mp4 file after convert
            print("Removing mp4 file...")
            if os.path.exists(location):
                os.remove(location)
                return 1
            else:
                print("The file does not exist") 

        except VideoUnavailable:
            return 0
