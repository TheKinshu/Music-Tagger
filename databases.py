import requests
import logging
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

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
        client_id = "2ecabf8ed1a1487584ef7fd9f78b5bc1"
        client_secret = "ff8156c2d45245688ccf2d25c7c9be97"
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

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

            return results['track']['name'], results['track']['artist']['name']

        except Exception as e:
            self.logger.error("Error getting data from database")
            self.logger.error(e)
            return None

    def find_album(self, songName, artistName):
        try:
            results = self.spotify.search(q='tack:' + f"{songName} + {artistName}", type='track')

            tracks = results['tracks']['items'][0]
            artists = [name['name'] for name in tracks['artists']]
            year = tracks['album']['release_date'].split("-")[0]
            if tracks['album']['album_type'] == "single":
                albumName = "single"
            else:
                albumName = tracks['album']['name']

            return albumName, artists, year

        except Exception as e:
            self.logger.error("Error getting data from database")
            self.logger.error(e)
            return None
