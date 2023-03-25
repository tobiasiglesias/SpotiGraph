from website import db
from website.models import Artist
from sqlalchemy.orm.exc import NoResultFound


def get_artist_db(id):
    try:
        return db.session.query(Artist).filter_by(id=id).one()
    except NoResultFound:
        return None


def add_artist_db(artist):
    # pass an artist object from the api
    query = get_artist_db(artist['id'])
    if query:
        return query
    else:
        print(artist)
        try:
            new_artist = Artist(
                id=artist['id'], name=artist['name'], image=artist['images'][0]['url'])
        except Exception as e:
            if len(artist['images']) < 1:
                new_artist = Artist(
                    id=artist['id'], name=artist['name'], image="https://picsum.photos/640")
        db.session.add(new_artist)
        db.session.commit()
        return new_artist
