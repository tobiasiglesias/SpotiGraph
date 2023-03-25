from website import db
from website.models import Track


def add_track_db(track):
    # pass track object from api
    query = get_track_db(track['id'])
    if query:
        return query
    else:
        new_track = Track(id=track['id'], name=track['name'])
        db.session.add(new_track)
        db.session.commit()
        return new_track


def get_track_db(id):
    return db.session.query(Track).filter_by(id=id).first()
