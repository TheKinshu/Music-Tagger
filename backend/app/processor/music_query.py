import requests

def search_recording(title, artist):
    base_url = f"https://musicbrainz.org/ws/2/recording/?query=recording:{title} AND artist:{artist}&fmt=json"
    headers = {
        "User-Agent": "MyMusicTagger/1.0 (youremail@example.com)"  # Replace with your email
    }
    params = {
        "query": f'recording:"{title}" AND artist:"{artist}"',
        "fmt": "json"
    }

    response = requests.get(base_url, headers=headers)
    # tests = "https://musicbrainz.org/ws/2/recording/?query=recording:%22%E5%8D%81%E6%88%92%EF%BC%881984%EF%BC%89%22%20AND%20artist:%22Ado%22&fmt=json"
    # f = requests.get(tests, headers=headers).json()

    if response.status_code == 200:
        data = response.json()
        recordings = data.get("recordings", [])
        return recordings

    return None
