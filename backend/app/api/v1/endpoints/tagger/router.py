import os
import re

from typing import Final, List

from fastapi import APIRouter, HTTPException
from structlog import get_logger

from backend.app.api.v1.endpoints.tagger.models import MusicList, MusicObject, Lyrics, LyricsRequest, LyricsTag

from backend.app.common.models import ErrorResponseModel, CommonResponse
from eyed3 import load

from backend.app.processor.lyrics_query import lyric_query
from backend.app.processor.music_query import search_recording

logger: Final = get_logger()

router = APIRouter(responses={403: {"model": ErrorResponseModel},
                              401: {"model": ErrorResponseModel},
                              400: {"model": ErrorResponseModel},
                              404: {"model": ErrorResponseModel}},
                   dependencies=[])


@router.post("/list", operation_id="MusicList")
async def music_list() -> MusicList:
    music_dir = './downloads'
    music_files = []

    for filename in os.listdir(music_dir):
        if filename.endswith(".mp3"):
            audio = load(music_dir + '/' + filename)

            audio_object = {
                'file_name': filename.replace('.mp3', ''),
                'title': audio.tag.title if audio.tag.title else '',
                'artist': audio.tag.artist if audio.tag.artist else '',
                'album': audio.tag.album if audio.tag.album else '',
                'album_artist': audio.tag.album_artist if audio.tag.album_artist else '',
                'release_date': str(audio.tag.release_date) if audio.tag.release_date else None,
                'genre': audio.tag.genre.name if audio.tag.genre else ''
            }

            try:
                music_files.append(MusicObject(**audio_object))
            except Exception as e:
                logger.error(f"Error creating MusicObject: {e}")
                continue

    return MusicList(music_list=music_files)

@router.post("/tag-lyrics", operation_id="TagLyrics")
async def tag_lyrics(lyric_tag: LyricsTag) -> CommonResponse:
    file_path = f"./downloads/{lyric_tag.music_object.file_name}.mp3"

    try:
        audio = load(file_path)
        audio.tag.lyrics.set(lyric_tag.lyrics)

        audio.tag.save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tagging music: {str(e)}")
    return CommonResponse(success=True)


@router.post("/tag-music", operation_id="TagMusic")
async def tag_music(music_object: MusicObject) -> CommonResponse:
    file_path = f"./downloads/{music_object.file_name}.mp3"

    try:
        audio = load(file_path)

        audio.tag.title = music_object.title
        audio.tag.artist = music_object.artist
        audio.tag.album = music_object.album
        audio.tag.album_artist = music_object.album_artist
        audio.tag.release_date = music_object.release_date
        audio.tag.genre = music_object.genre

        audio.tag.save()

        # update file name
        new_file_path = f"./downloads/{music_object.title} - {music_object.artist}.mp3"

        if file_path != new_file_path:
            os.rename(file_path, new_file_path)
            logger.info(f"Renamed file from {file_path} to {new_file_path}")


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tagging music: {str(e)}")
        pass
    return CommonResponse(success=True)


@router.post("/query-music", operation_id="QueryMusic")
async def query_music(music_object: MusicObject) -> List[MusicObject]:
    final_results = []

    if len(music_object.title) > 0:
        music_title = music_object.title

    else:
        music_title = music_object.file_name.strip()

    results = search_recording(music_title, music_object.artist)

    if results:
        for query in results:
            data = MusicObject(
                file_name=music_object.file_name,
                title=query['title'],
                artist=query['artist-credit'][0]['name'] if query['artist-credit'] else '',
                album_artist=query['releases'][0]['title'] if query.get('releases') else '',
                album=query['releases'][0]['title'] if query.get('releases') else '',
                release_date=query['first-release-date'] if query.get('first-release-date') else None,
                genre=query.get('genres', '')
            )
            final_results.append(data)

    if not results:
        match = re.match(r'【(.*?)】(.*?)（(\d{4})）(.*)', music_title)
        for word in match.groups():
            results = search_recording(word, music_object.artist)
            if results:
                for query in results:
                    try:
                        title = query['title']

                        if not title in music_title:
                            continue

                        artist = query['artist-credit'][0]['name'] if query['artist-credit'] else ''
                        album_artist = query['releases'][0]['title'] if query.get('releases') else ''
                        album = query['releases'][0]['title'] if query.get('releases') else ''
                        release_date = query['first-release-date'] if query.get('first-release-date') else None

                        genre = query.get('genres', '')

                        data = MusicObject(
                            file_name=music_object.file_name,
                            title=title,
                            artist=artist,
                            album_artist=album_artist,
                            album=album,
                            release_date=release_date,
                            genre=genre
                        )
                        final_results.append(data)
                    except Exception as e:
                        logger.error(f"Error creating MusicObject: {e}")
                        continue

    return final_results


@router.post("/query-lyrics", operation_id="QueryLyrics")
async def query_lyrics(lyric_request: LyricsRequest) -> Lyrics:
    """
    Query lyrics for the given music object.
    :param artist:
    :param title:
    :return: Lyrics as a string.
    """

    lyrics = await lyric_query(lyric_request.artist, lyric_request.song_title, lyric_request.url)

    if not lyrics:
        raise HTTPException(status_code=404, detail="Lyrics not found.")

    return Lyrics(success=True, lyrics=lyrics)


