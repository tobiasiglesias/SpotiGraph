from website.utils import get_artist, get_all_albums, get_collaborators
from website import create_app
from flask import jsonify
from flask_cors import CORS


app = create_app()
CORS(app)


@app.route('/artist/<string:name>')
def artist(name):
    print(get_artist(name)['id'])
    return jsonify(get_artist(name))


# @app.route('/artist/tracks/<string:name>')
# def tracks(name):
#     tracks = get_all_tracks_from_api(name)
#     print(len(tracks))
#     return tracks


@app.route('/artist/albums/<string:name>')
def albums(name):
    artist = get_artist(name)
    albums = get_all_albums(artist)
    return albums


@app.route('/artist/collabs/<string:name>')
def collabs(name):
    # TODO Serializar la lista de colaboradores
    hola = get_collaborators(name)
    return "get_collaborators(name)"


if __name__ == '__main__':
    app.run(debug=True)
