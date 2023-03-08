from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import spotipy


url = 'https://api.spotify.com/v1/search?type=track&q=artist:'


load_dotenv()


client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET')
)

# Inicializar objeto de autenticación de Spotify
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

###


def get_access_token():
    import base64
    import requests
    import json

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    # encode auth
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

