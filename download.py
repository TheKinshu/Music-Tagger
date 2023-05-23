from pytube import YouTube, Playlist, cli
from pytube.exceptions import VideoUnavailable
import requests, os, logging as log
from moviepy.video.io.VideoFileClip import VideoFileClip
import time
class Download():
    # 
    def __init__(self, URL=None, playlist=None, window=None) -> None:

        log.basicConfig(filename='debug.log', level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.window = window
        self.download_location = "./Downloads/"
        if not URL == None:
            self.yt = YouTube(URL, on_progress_callback=cli.on_progress)
        if not playlist == None:
            self.yt_playlist = Playlist(playlist)
        self.music_title = ""
        self.thumbnail_url = ""
        self.regex = ['/', '\\', '?', '<', '>', '?', '*', '"', '|', ':', '.', ',', "'", '#', '$', ';']
        self.failed_songs = []
        self.fail_count = 0
    #
    def download_playlist(self, should_delete, resolution="360p"):
        for video in self.yt_playlist.videos:
            try:
                self.music_title = video.title
            except VideoUnavailable:
                self.fail_count += 1
                self.failed_songs.append(self.music_title)
                continue
            except Exception:
                continue
            finally:
                
                # Download Video
                stream = video.streams.filter(file_extension='mp4', res=resolution).first()
                stream.download(self.download_location)
                
                self.music_title = video.title
                self.thumbnail_url = video.thumbnail_url
                # Find all the character not allow for file naming
                for i in self.regex:
                    if i in self.music_title:
                        log.debug("{} character has been found in the title and is being deleted!".format(i))
                        self.music_title = self.music_title.replace(i, "")

                self.download_thumbnail()

                # Location of mp4 
                location = "{}{}".format(self.download_location, self.music_title)
                    
                self.convert_video(location, should_delete)   
    #
    def download_link(self, should_delete, resolution="360p"):
        try:
            log.debug("Finding Video....")
            self.music_title = self.yt.title
            self.thumbnail_url = self.yt.thumbnail_url
            log.debug("Video Found!")
    
            # Find all the character not allow for file naming
            for i in self.regex:
                if i in self.music_title:
                    log.debug("{} character has been found in the title and is being deleted!".format(i))
                    self.music_title = self.music_title.replace(i, "")
            self.download_thumbnail()
            self.window.update()
            log.debug("Downloading Video please wait......")
            stream = self.yt.streams.filter(file_extension='mp4', res=resolution).first()
            stream.download(self.download_location)
            self.window.update()
    
            log.debug("Download complete!")
            # Location of mp4 
            location = "{}{}".format(self.download_location, self.music_title)
            
            self.convert_video(location, should_delete)

        except VideoUnavailable:
            return 0
    #
    def download_thumbnail(self):
        with open("thumbnail\\{}.jpg".format(self.music_title), 'wb') as handle:
            response = requests.get(self.thumbnail_url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    #
    def convert_video(self, location, should_delete):
        # Convert video to audio
        log.debug("Converting audio....")
        try:
            self.window.update()
            video = VideoFileClip("{}.mp4".format(location))
            self.window.update()
            video.audio.write_audiofile("{}/{}.mp3".format(self.download_location, self.music_title))
            self.window.update()
            video.close()
            self.window.update()
        except OSError:
            self.fail_count += 1
            self.failed_songs.append(self.music_title)
        finally:
            if should_delete: 
                self.delete_video("{}.mp4".format(location))
        log.debug("Conversion complete!") 

    #
    def delete_video(self, location):
        # Remove mp4 file after convert
        log.debug("Removing mp4 file...")
        if os.path.exists(location):
            os.remove(location)
            return 1
        else:
            return 0
            #print("The file does not exist")
