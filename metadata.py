from utils import api_get, fetch_bytes, sleep_api

def search_musicbrainz(artist, title):
    """Searches for a song's info on MusicBrainz."""
    from urllib.parse import quote
    query = quote(f'{artist} {title}')
    url = f"https://musicbrainz.org/ws/2/recording/?query={query}&fmt=json&limit=3"
    data = api_get(url)
    sleep_api()

    if not data or 'recordings' not in data or not data['recordings']:
        return None

    rec = data['recordings'][0]
    result = {}

    # Year
    if rec.get('first-release-date'):
        result['DATE'] = rec['first-release-date'][:4]

    # Genre (from MusicBrainz tags)
    if rec.get('tags'):
        genres = sorted(rec['tags'], key=lambda x: x.get('count', 0), reverse=True)
        if genres:
            result['GENRE'] = genres[0]['name'].title()

    # Album
    releases = rec.get('releases', [])
    if releases:
        result['ALBUM'] = releases[0].get('title', '')
        result['_mbid'] = releases[0].get('id', '')

    # Track number
    if rec.get('position'):
        result['TRACKNUMBER'] = str(rec['position'])

    return result

def search_itunes(artist, title):
    """Searches the iTunes API as a fallback."""
    from urllib.parse import quote
    query = quote(f'{artist} {title}')
    url = f'https://itunes.apple.com/search?term={query}&entity=song&limit=1'
    data = api_get(url)
    sleep_api()

    if not data or 'results' not in data or not data['results']:
        return None

    song = data['results'][0]
    result = {}

    # Year
    if song.get('releaseDate'):
        result['DATE'] = song['releaseDate'][:4]

    # Genre
    if song.get('primaryGenreName'):
        result['GENRE'] = song['primaryGenreName']

    # Album
    if song.get('collectionName'):
        result['ALBUM'] = song['collectionName']

    # Track number
    if song.get('trackNumber'):
        result['TRACKNUMBER'] = str(song['trackNumber'])

    # Cover URL
    if song.get('artworkUrl100'):
        result['cover_url'] = song['artworkUrl100'].replace('100x100bb', '600x600bb')

    return result

def fetch_cover_art(mbid):
    """Downloads cover art from the Cover Art Archive."""
    if not mbid:
        return None
    url = f"https://coverartarchive.org/release/{mbid}/front-500"
    data = fetch_bytes(url)
    sleep_api()
    return data
