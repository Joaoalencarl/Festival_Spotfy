import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri
        self.sp = None

    def authenticate(self, scope):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.__client_id,
                client_secret=self.__client_secret,
                redirect_uri=self.__redirect_uri,
                scope=scope
            )
        )
