from datetime import datetime
from typing import List

from backend.app.common.models import StrictBaseModel, CommonResponse


class MusicObject(StrictBaseModel):
    file_name: str
    title: str
    artist: str
    album: str
    album_artist: str
    release_date: str | None
    genre: str

class MusicList(StrictBaseModel):
    music_list: List[MusicObject]

class Lyrics(CommonResponse):
    lyrics: str

class LyricsRequest(StrictBaseModel):
    artist: str
    song_title: str
    url: str | None = None

class LyricsTag(StrictBaseModel):
    music_object: MusicObject
    lyrics: str