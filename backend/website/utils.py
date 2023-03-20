from .crud.collabs import get_collabs_db
from .crud.artists import get_artist_db


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


def make_node(artist, main_artist):
    obj = {}
    obj['id'] = artist.id
    obj['name'] = artist.name
    obj['image_url'] = artist.image
    if artist == main_artist:
        obj['main_artist'] = True
    else:
        obj['main_artist'] = False

    return obj


def get_nodes_collabs(collabs, main_artist):
    main_artist_obj = get_artist_db(main_artist['id'])
    collabs = list(map(lambda artist: get_artist_db(artist.id), collabs))
    if main_artist_obj not in collabs:
        collabs.append(main_artist_obj)
    collabs = list(map(lambda artist: make_node(
        artist, main_artist_obj), collabs))

    return collabs


def get_links_collabs(nodes, main_artist):
    links = list(
        map(lambda artist: {'source': main_artist['id'], 'target': artist['id']}, nodes))
    return links


# Para endpoints


def get_dict_collab(main_artist):
    # collab_object = {}
    # collab_object['id'] = main_artist['id']
    # collab_object['name'] = main_artist['name']
    # collab_object['images'] = main_artist['images']
    # collab_object['collabs'] = get_collabs_id(
    #     get_collabs_db(main_artist), main_artist['id'])
    # return collab_object

    collab_object = {}
    collabs = get_collabs_db(main_artist)
    nodes = get_nodes_collabs(collabs, main_artist)
    collab_object['nodes'] = nodes
    collab_object['links'] = get_links_collabs(nodes, main_artist)
    return collab_object
