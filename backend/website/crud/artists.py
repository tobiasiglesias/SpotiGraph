from website import session
from website.models import Artist


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
