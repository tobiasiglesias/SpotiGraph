from .crud.collabs import get_collabs_db


def get_multi_artist_tracks(tracks):
    multi_artist_tracks = []
    for track in tracks:
        if len(track['artists']) > 1:
            multi_artist_tracks.append(track)
    return multi_artist_tracks


def flatten_tracks_list(tracks):
    flattened_tracks = []
    for album in tracks:
        for track in album['items']:
            flattened_tracks.append(track)
    return flattened_tracks


def get_track_names(tracks):
    return list(map(lambda track: track['name'], tracks))


def get_collabs_id(collabs, main_artist_id):
    collabs = list(filter(lambda artist: artist.id != main_artist_id, collabs))
    return list(map(lambda artist: artist.id, collabs))


# Para endpoints


def get_dict_collab(main_artist):
    collab_object = {}
    collab_object['id'] = main_artist['id']
    collab_object['name'] = main_artist['name']
    collab_object['images'] = main_artist['images']
    collab_object['collabs'] = get_collabs_id(
        get_collabs_db(main_artist), main_artist['id'])
    return collab_object
