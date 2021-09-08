from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
from moviepy.video.io.VideoFileClip import VideoFileClip

import requests, os

class Download():
    def __init__(self, URL=None, playlist=None) -> None:
        self.download_location = "./Downloads/"
        if not URL == None:
            self.yt = YouTube(URL)
        if not playlist == None:
            self.yt_playlist = Playlist(playlist)
        self.music_title = ""
        self.thumbnail_url = ""
        self.regex = ['/', '\\', '?', '<', '>', '?', '*', '"', '|', ':', '.', ',', "'", '#']
    
    def download_playlist(self, should_delete, resolution):
        try:
            for video in self.yt_playlist.videos:
                self.music_title = video.title
                self.thumbnail_url = video.thumbnail_url

                # Find all the character not allow for file naming
                for i in self.regex:
                    if i in self.music_title:
                        #print("{} character has been found in the title and is being deleted!".format(i))
                        self.music_title = self.music_title.replace(i, "")

                self.download_thumbnail()

                if should_delete:
                    stream = video.streams.filter(file_extension='mp4').first()
                    stream.download(self.download_location)
                else:
                    stream = video.streams.filter(file_extension='mp4', res=resolution).first()
                    stream.download(self.download_location)

                # Location of mp4 
                location = "{}{}".format(self.download_location, self.music_title)
                
                self.convert_video(location)
                
                if should_delete: 
                    self.delete_video("{}.mp4".format(location))

        except VideoUnavailable:
            return 0

    def download_link(self, should_delete, resolution):
        try:
            #print("Finding Video....")
            self.music_title = self.yt.title
            self.thumbnail_url = self.yt.thumbnail_url
            #print("Video Found!")

            # Find all the character not allow for file naming
            for i in self.regex:
                if i in self.music_title:
                    #print("{} character has been found in the title and is being deleted!".format(i))
                    self.music_title = self.music_title.replace(i, "")
            self.download_thumbnail()

            #print("Downloading Video please wait......")
            if should_delete:
                stream = self.yt.streams.filter(file_extension='mp4').first()
                stream.download(self.download_location)
            else:
                stream = self.yt.streams.filter(file_extension='mp4', res=resolution).first()
                stream.download(self.download_location)
            #print("Download complete!")

            # Location of mp4 
            location = "{}{}".format(self.download_location, self.music_title)
            
            self.convert_video(location)
            
            if should_delete: 
                self.delete_video("{}.mp4".format(location))

        except VideoUnavailable:
            return 0

    def download_thumbnail(self):
        with open("thumbnail\\{}.jpg".format(self.music_title), 'wb') as handle:
            response = requests.get(self.thumbnail_url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    def convert_video(self, location):
        # Convert video to audio
        #print("Converting audio....")
        video = VideoFileClip("{}.mp4".format(location))
        video.audio.write_audiofile("{}/{}.mp3".format(self.download_location, self.music_title))
        video.close()
        #print("Conversion complete!") 


    def delete_video(self, location):
        # Remove mp4 file after convert
        #print("Removing mp4 file...")
        if os.path.exists(location):
            os.remove(location)
            return 1
        else:
            return 0
            #print("The file does not exist")
