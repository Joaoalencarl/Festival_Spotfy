import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()


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


class PlaylistManager(SpotifyClient):
    def create_playlist(self, user, name, description, public):
        return self.sp.user_playlist_create(
            user=user,
            name=name,
            description=description,
            public=public
        )

    def add_tracks_to_playlist(self, playlist_id, track_uris):
        self.sp.playlist_add_items(playlist_id, track_uris)


class EventPlaylistCreator(PlaylistManager):
    def collect_artist_information(self):
        artists = input("Digite o nome dos artistas (separados por vírgula): ").split(',')
        return artists

    def create_event_playlist(self, user, playlist_name, event_day):
        artists = self.collect_artist_information()

        playlist = self.create_playlist(
            user=user,
            name=playlist_name,
            description=f'Esquenta! o {playlist_name} é dia {event_day}',
            public=True
        )
        playlist_id = playlist['id']

        for artist in artists:
            results = self.sp.search(q='artist:' + artist, type='artist', limit=1)
            if len(results['artists']['items']) > 0:
                artist_id = results['artists']['items'][0]['id']
                top_tracks = self.sp.artist_top_tracks(artist_id)
                track_uris = [track['uri'] for track in top_tracks['tracks'][:10]]
                self.add_tracks_to_playlist(playlist_id, track_uris)

        playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
        print("Link da playlist:", playlist_url)


# Usage example
if __name__ == "__main__":
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    event_playlist_creator = EventPlaylistCreator(client_id, client_secret, redirect_uri)
    event_playlist_creator.authenticate('playlist-modify-public')

    username = input("Digite o nome do usuário: ")
    playlist_name = input("Digite o nome do seu próximo evento: ")
    event_day = input("Digite a data do seu evento: ")

    event_playlist_creator.create_event_playlist(username, playlist_name, event_day)
