import spotipy
import os

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = "a481aa2eb31248c39a5ea009c28c1d9d"
CLIENT_SECRET = "b1a9a9e2c64c41839a1126e8aa722ee6"
REDIRECT_URI = "http://localhost:8000"

# Configuraçãod
scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))


# Coletando as informações da playlist
playlist_name = input("Digite o nome da playlist: ")
playlist_description = input("Digite a descrição da playlist: ")
artists = []

while True:
    artist = input("Digite o nome do artista (ou 'fim' para encerrar): ")
    if artist.lower() == "fim":
        break
    artists.append(artist)

# Criando a playlist
user = sp.current_user()["id"]
playlist = sp.user_playlist_create(
    user, playlist_name, public=True, description=playlist_description)
playlist_id = playlist["id"]

# Pesquisando e adicionando faixas à playlist
for artist in artists:
    results = sp.search(q='artist:' + artist, type='artist')
    if len(results['artists']['items']) > 0:
        artist_id = results['artists']['items'][0]['id']
        top_tracks = sp.artist_top_tracks(artist_id)
        track_uris = [track['uri'] for track in top_tracks['tracks'][:10]]
        sp.playlist_add_items(playlist_id, track_uris)

# Obtendo o link da playlist
playlist_url = playlist["external_urls"]["spotify"]
print("Playlist criada com sucesso!")
print("Acesse a playlist aqui: " + playlist_url)
