import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from .auth import sp, get_access_token
import requests
from flask import json
from . import session
from .models import Track, Colab, Artist
from datetime import datetime, timedelta


def get_artist(name):
    # Buscar artista en Spotify
    result = sp.search(q=name, type='artist')
    items = result['artists']['items']
    if len(items) > 0:
        artist = items[0]
        return artist
    else:
        return {}


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


def get_collab_db(id1, id2):

    return session.query(Colab).filter_by(artist1_id=min(id1, id2), artist2_id=max(id1, id2)).first()


def get_all_collaborators_db(artist_id):
    collaborators = (
        session.query(Artist)
        .join(Colab, (Artist.id == Colab.c.artist1_id) | (Artist.id == Colab.c.artist2_id))
        .filter((Colab.c.artist1_id == artist_id) | (Colab.c.artist2_id == artist_id))
        .all()
    )
    return collaborators


def add_collab_db(artist, other_artist):
    query = get_collab_db(artist.id, other_artist.id)
    if query:
        return query
    else:
        new_colab = Colab.insert().values(artist1_id=min(artist.id, other_artist.id),
                                          artist2_id=max(artist.id, other_artist.id))
        session.execute(new_colab)
        session.commit()
        return new_colab


def get_artist_db(id):
    return session.query(Artist).filter_by(id=id).first()


def add_artist_db(artist):
    # pass an artist object from the api
    query = get_artist_db(artist['id'])
    if query:
        return query
    else:
        new_artist = Artist(id=artist['id'], name=artist['name'])
        session.add(new_artist)
        session.commit()
        return new_artist


def get_track_db(id):
    return session.query(Track).filter_by(id=id).first()


def add_track_db(track):
    # pass track object from api
    query = get_track_db(track['id'])
    if query:
        return query
    else:
        new_track = Track(id=track['id'], name=track['name'])
        session.add(new_track)
        session.commit()
        return new_track


def add_collabs(artist_name, limit=50, offset=0):

    # TODO Manejar esto con la db cuando este

    result = sp.search(q=artist_name + ' feat',
                       type='track', limit=50, offset=0)
    tracks = result['tracks']['items']

    # Pueden no ser todos los temas, ojala que si

    for i in range(15):
        result = sp.search(q=artist_name + ' feat',
                           type='track', limit=50, offset=50 * i)
        tracks.extend(result['tracks']['items'])

    main_artist = get_artist(artist_name)
    query = get_artist_db(main_artist['id'])
    if query:
        main_artist = query
    else:
        main_artist = Artist(
            id=main_artist['id'], name=main_artist['name'], complete_node=True)
        session.add(main_artist)
        session.commit()

    # Nos quedamos con los temas unicamente del artista

    artist_tracks = []

    # Agregar canciones del artista con mas de 1 artista

    for track in tracks:
        artists = track['artists']
        artists_ids = [a['id'] for a in artists]
        if main_artist.id in artists_ids and len(artists) > 1:
            artist_tracks.append(track)

    # Create db objects

    for track in artist_tracks:
        for artist_in_track in track['artists']:
            if artist_in_track['id'] != main_artist.id:
                # Check if artist exists in db
                query = get_artist_db(artist_in_track['id'])
                if query:
                    # check colab
                    colab = get_collab_db(query.id, main_artist.id)
                    if colab:
                        continue
                    else:
                        add_collab_db(main_artist, query)
                else:
                    other_artist = add_artist_db(artist_in_track)
                    add_track_db(track)
                    add_collab_db(main_artist, other_artist)

    return


def get_collabs_db(artist_name):
    artist = get_artist(artist_name)
    query = get_artist_db(artist['id'])
    if query and query.complete_node and (datetime.now() - query.last_upadte < timedelta(days=30)):
        # devolver todos los artistas que colaboraron con artist
        collabs = get_all_collaborators_db(query.id)
        print(collabs)
        return collabs
    else:
        add_collabs(artist_name)
        return get_collabs_db(artist_name)


def get_collaborators(artist_name):
    return get_collabs_db(artist_name)
