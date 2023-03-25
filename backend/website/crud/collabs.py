from website import db
from website.api import get_artist_from_name, get_feat_tracks, get_artist_from_id
from website.models import Colab, Artist
from .artists import get_artist_db, add_artist_db
from .tracks import add_track_db
from datetime import datetime, timedelta


def get_collab_db(id1, id2):

    return db.session.query(Colab).filter_by(artist1_id=min(id1, id2), artist2_id=max(id1, id2)).first()


def get_all_collaborators_db(artist_id):
    collaborators = (
        db.session.query(Artist)
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
        # new_colab = Colab.insert().values(artist1_id=min(artist.id, other_artist.id),
        #                                   artist2_id=max(artist.id, other_artist.id))
        # db.session.execute(new_colab)
        # db.session.commit()
        try:
            new_colab = Colab.insert().values(artist1_id=min(artist.id, other_artist.id),
                                              artist2_id=max(artist.id, other_artist.id))
            db.session.execute(new_colab)
            db.session.commit()
        except:
            db.session.rollback()

        return new_colab


def get_collabs_db(artist):
    query = get_artist_db(artist['id'])
    if query and query.complete_node and (datetime.now() - query.last_upadte < timedelta(days=30)):
        # devolver todos los artistas que colaboraron con artist
        collabs = get_all_collaborators_db(query.id)
        return collabs
    else:
        add_collabs(artist)
        return get_collabs_db(artist)


def add_collabs(main_artist, limit=50, offset=0):

    # TODO Manejar esto con la db cuando este

    tracks = get_feat_tracks(main_artist, 0)

    # Pueden no ser todos los temas, ojala que si

    for i in range(1, 15):
        result = get_feat_tracks(artist=main_artist, offset=50 * i)
        tracks.extend(result)

    query = get_artist_db(main_artist['id'])
    if query:
        main_artist = query
        main_artist.complete_node = True
        main_artist.last_upadte = datetime.now()
        db.session.add(main_artist)
        db.session.commit()
    else:
        main_artist = add_artist_db(main_artist)

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
                    other_artist = get_artist_from_id(artist_in_track['id'])
                    other_artist = add_artist_db(other_artist)
                    add_track_db(track)
                    add_collab_db(main_artist, other_artist)

    return


# NEGRADA INCOMING

def get_artist_from_name2(artist_name):
    return get_artist_from_name(artist_name)
