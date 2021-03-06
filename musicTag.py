import requests
from eyed3 import load
from eyed3.id3 import Tag
class MusicTag():
    #
    def __init__(self, title = None) -> None:
        self.title = title
        self.musicbrainz_endpoint = "https://musicbrainz.org/ws/2/release-group/?limit=5&fmt=json&query="
        self.headers = {    'Content-Type': 'application/json',
                            "Authorization": "Discogs key=FIvcpCrDXyemGBiyfJdj, secret=xovpybPirVGpuCfDlOFLhuiklCIoklpz"
        }
        self.music = []
        self.songs = []
    #
    def search(self):
        music_reponse = requests.get(self.musicbrainz_endpoint+"{}".format(self.title))
        music_reponse.raise_for_status()
        self.songs = music_reponse.json()['release-groups']

        artists = []
        for song in self.songs:
            artist = []
            for i in range(len(song['artist-credit'])):
                by = song['artist-credit'][i]['artist']['name']
                artist.append(str(by).replace(',',''))
            artists.append(artist)     

        for i in range(len(self.songs)):
            dis_end_point = "https://api.discogs.com/database/search?release_title={}".format(self.songs[i]['title'])
            #dis_end_point = "https://api.discogs.com/database/search?q={{q={}}}".format(self.songs[i]['title'])
            dis_response = requests.get(dis_end_point,headers=self.headers)

            release_date = None

            dis_response.raise_for_status()
            try:
                genre = dis_response.json()['results'][0]['genre'][0]
                release_date = self.songs[i]['first-release-date']
                release_year = str(self.songs[i]['first-release-date']).split("-")
                album = self.songs[i]['primary-type']
            except IndexError:
                genre = ""
                release_date = ""
                release_year = [[]]
                album = ""
            except KeyError:
                genre = ""
                release_date = ""
                release_year = [[]]
                album = ""

            music_details = {
                "Title": self.songs[i]['title'],
                "Year": release_year[0],
                "Release-Date": release_date,
                "Album": album,
                "Contributing": artists[i],
                "Artist": artists[i][0],
                "Genre": genre
            }
            self.music.append(music_details)

        return self.music
        
    #
    def tagInfo(self, detail, lyric):
        t = Tag()
        t.lyrics.set(lyric)
        t.save("Downloads/{}".format(self.title))
        audiofile = load("Downloads/{}".format(self.title))
        
        audiofile.tag.title = detail["Title"]
        audiofile.tag.album_artist = detail["Artist"]
        audiofile.tag.album = detail["Album"]
        if not len(detail["Contributing"]) > 1:
            audiofile.tag.artist = detail["Artist"]
        else:
            audiofile.tag.artist = ", ".join(detail["Contributing"])


        audiofile.tag.release_date = detail['Release-Date']
        audiofile.tag.year = detail["Year"]
        audiofile.tag.genre = detail["Genre"]

        audiofile.tag.save()