from utils import api_get, sleep_api

def fetch_lyrics_lrclib(artist, title, album="", duration=0):
    """Searches for lyrics on LRCLIB (free API, no key required)."""
    from urllib.parse import urlencode
    params = urlencode({
        'artist_name': artist,
        'track_name': title,
        'album_name': album,
        'duration': int(duration)
    })
    url = f"https://lrclib.net/api/get?{params}"
    data = api_get(url)
    sleep_api()

    if not data:
        return None

    # Prefer plain lyrics over synced (timestamped) lyrics
    return data.get('plainLyrics') or data.get('syncedLyrics')

def fetch_lyrics_fallback(artist, title):
    """Searches for lyrics on lyrics.ovh as a fallback."""
    from urllib.parse import quote
    artist_enc = quote(artist)
    title_enc = quote(title)
    url = f"https://api.lyrics.ovh/v1/{artist_enc}/{title_enc}"
    data = api_get(url)
    sleep_api()

    if data and 'lyrics' in data:
        return data['lyrics']
    return None

def fetch_lyrics_chartlyrics(artist, title):
    """Searches for lyrics on ChartLyrics as a third fallback."""
    from urllib.parse import quote
    url = f"http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist={quote(artist)}&song={quote(title)}"
    data = api_get(url)
    sleep_api()

    if data and data.get('Lyric'):
        return data['Lyric']
    return None
