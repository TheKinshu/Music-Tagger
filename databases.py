import requests
import logging
from pprint import pprint


# Using REST API to get data from the database
class Database:
    def __init__(self, logger=None, title=None, artist=None, method=None):
        self.logger = logger
        self.trackTitle = title
        self.lastFmAPIKey = "4e4a56c1fbdbbcc9e78404d2a2509b6b"
        self.dicogsKey = "FIvcpCrDXyemGBiyfJdj"
        self.discogsSecret = "xovpybPirVGpuCfDlOFLhuiklCIoklpz"
        self.method = f"track.{method}"
        self.link = "http://ws.audioscrobbler.com"
        self.artist = artist
        self.lastFmAPIUrl = f"{self.link}/2.0/?method={self.method}&format=json&api_key={self.lastFmAPIKey}"
        self.discogsAPUrl = "https://api.discogs.com/database/search?q="


    def get_artist_with_song_name(self):
        try:
            url = self.lastFmAPIUrl + f"&track={self.trackTitle}"
            r = requests.get(url)

            # check status
            if r.status_code != 200:
                self.logger.error("Error getting data from database")
                return None

            # Get list of data
            results = r.json()

            nameWithArtist = []

            for track in results["results"]["trackmatches"]["track"]:
                nameWithArtist.append({
                    "name": track["name"],
                    "artist": track["artist"]
                })

            return nameWithArtist

        except Exception as e:
            self.logger.error("Error getting data from database")
            self.logger.error(e)
            return None

    def get_music_tag(self):
        try:
            url = self.lastFmAPIUrl + f"&artist={self.artist}&track={self.trackTitle}"
            r = requests.get(url)

            # check status
            if r.status_code != 200:
                self.logger.error("Error getting data from database")
                return None

            # Get list of data
            results = r.json()

            tags = []

            for tag in results["toptags"]["tag"]:
                tags.append(tag["name"])

            return tags

        except Exception as e:
            self.logger.error("Error getting data from database")
            self.logger.error(e)
            return None

    def find_album(self):
        try:
            url = self.discogsAPUrl + f"{self.artist}+{self.trackTitle}&type=release&key={self.dicogsKey}&secret={self.discogsSecret}"
            r = requests.get(url)

            # check status
            if r.status_code != 200:
                self.logger.error("Error getting data from database")
                return None

            # Get list of data
            results = r.json()

            albums = []

            for album in results["results"]:
                albums.append({
                    "title": album["title"],
                    "year": album["year"],
                    "id": album["id"]
                })

            return albums

        except Exception as e:
            self.logger.error("Error getting data from database")
            self.logger.error(e)
            return None
