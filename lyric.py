import requests, lxml, re, os
from bs4 import BeautifulSoup
from pprint import pprint
class Lyric():
    def __init__(self, search="") -> None:
        self.search = search
        self.api_key = "BPJ2z-UF99DecoxWNNHGzn_J4sodcQ794ZMt5_VV-8z0SanjgeSSv86kRrvTNkDq"
        self.end_point = "http://api.genius.com/search?q={}&access_token={}".format(self.search, self.api_key)

    def find_lyrics(self):
        response = requests.get(self.end_point)

        response.raise_for_status()

        url = (response.json()["response"]["hits"][0]["result"]["url"])

        response = requests.get(url)

        response.raise_for_status()
        lyric_page = response.text

        soup = BeautifulSoup(lyric_page, "lxml")

        song = ""

        for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):

            for i in tag.select('i'):
                i.unwrap()
            tag.smooth()

            line = tag.get_text(strip=True, separator='\n')
            song = song + line


        song = re.sub(r"[\[].*?[\]]", "", song)

        song = os.linesep.join([s for s in song.splitlines() if s])

        self.write_to_txt(song)
        pprint(song)
        return song

    def write_to_txt(self, song):
        with open("lyrics.txt", "w",  encoding='utf-8') as f:
            f.write(song)
