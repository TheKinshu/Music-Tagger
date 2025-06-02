import time

from azapi import AZlyrics, tools
from azapi.tools import normalGet
from selenium.webdriver.common.by import By
from structlog import get_logger
from typing import Final
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

logger: Final = get_logger()

options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--disable-gpu")  # Optional: needed on Windows
options.add_argument("--no-sandbox")  # Optional: needed in some environments


async def selenium_lyric_query(artist: str, song_title: str, url: str) -> str:
    artist = artist.lower().replace(" ", "")
    song = song_title.lower().replace(" ", "")

    if url:
        url = url.strip()
    else:
        url = f"https://www.azlyrics.com/lyrics/{artist}/{song}.html"

    # Headless Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    lyrics = None

    try:
        driver.get(url)
        time.sleep(2)  # Wait for page to fully load

        # The lyrics are inside a div that doesn't have a class or id
        divs = driver.find_elements(By.XPATH, "//div[not(@class) and not(@id)]")
        for div in divs:
            if len(div.text.splitlines()) > 5:  # crude check to find lyrics block
                lyrics = div.text
                break

    finally:
        driver.quit()

    return lyrics if lyrics else "Lyrics not found."


async def lyric_query(artist: str, title: str, url: str = '') -> str:


    return await selenium_lyric_query(artist, title, url)


    # try:
    #
    #     driver = webdriver.Chrome(options=options)
    #     driver.get("https://www.azlyrics.com/lyrics/queen/bohemianrhapsody.html")
    #
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')
    #
    #     lyrics_divs = soup.find_all("div", class_=None)
    #     results = []
    #     for div in lyrics_divs:
    #         lyrics = div.get_text(separator="\n").strip()
    #         if len(lyrics) > 0:
    #             results.append(lyrics)
    #         print(lyrics)
    #
    # except Exception as e:
    #     print("Error:", e)
    #
    # finally:
    #     if driver:
    #         driver.quit()

    # try:
    #     logger.info("Fetching lyrics", artist=artist, title=title)
    #     lyrics = api.getLyrics(url=link)
    #
    #     if type(lyrics) == str:
    #         logger.info("Lyrics fetched successfully", artist=artist, title=title)
    #         return lyrics
    #     else:
    #         return ''
    # except Exception as e:
    #     logger.error(f"Error fetching lyrics: {e}", artist=artist, title=title)
    #     return ''
