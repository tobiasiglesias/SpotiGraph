from website.crud.collabs import get_collabs_db, get_artist_from_name2
from website.utils import get_dict_collab
from website import create_app
from flask import jsonify
from flask_cors import CORS


app = create_app()
CORS(app)


@app.route('/artist/<string:name>')
def artist(name):
    print(get_artist_from_name2(name)['id'])
    return jsonify(get_artist_from_name2(name))


# @app.route('/artist/tracks/<string:name>')
# def tracks(name):
#     tracks = get_all_tracks_from_api(name)
#     print(len(tracks))
#     return tracks


@app.route('/artist/albums/<string:name>')
def albums(name):
    artist = get_artist_from_name2(name)
    return albums


@app.route('/artist/collabs/<string:name>')
def collabs(name):
    # TODO Serializar la lista de colaboradores
    artist = get_artist_from_name2(name)
    return jsonify(get_dict_collab(artist))


if __name__ == '__main__':
    app.run(debug=True)
