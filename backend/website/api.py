from .auth import sp


def get_feat_tracks(artist, offset):
    artist_name = artist['name']
    result = sp.search(q=artist_name + ' feat',
                       type='track', limit=50, offset=offset)
    return result['tracks']['items']


def get_artist_from_name(name):
    # Buscar artista en Spotify
    result = sp.search(q=name, type='artist')
    items = result['artists']['items']
    if len(items) > 0:
        artist = items[0]
        return artist
    else:
        return {}


def get_artist_from_id(id):
    return sp.artist(id)


def get_all_albums(artist):
    last_albums = sp.artist_albums(
        artist_id=artist['id'], album_type='appears_on')
    albums = last_albums['items']
    while last_albums['next']:
        last_albums = sp.next(last_albums)
        albums.extend(last_albums['items'])
    return albums


def get_tracks_from_album(album):
    tracks = sp.album_tracks(album_id=album['id'])
    return tracks
