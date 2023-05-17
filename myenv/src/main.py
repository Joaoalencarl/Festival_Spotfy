import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

# Criação de um objeto de autenticação do Spotify
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret, 
                                               redirect_uri=redirect_uri, 
                                               scope=scope))

# Coletando as informações da playlist
artistas = input("Digite o nome dos artistas (separados por vírgula): ").split(',')

# Criando a playlist
nome_playlist = input("Digite o nome do seu próximo evento: ")
event_day = input("Digite a data do seu evento: ")
playlist = sp.user_playlist_create(user='31fv3cdnt4rngts2i4gtdiproeta', name=nome_playlist,
                                   description=f'Esquenta! o {nome_playlist} é dia {event_day}',
                                   public=True)
playlist_id = playlist['id']

# Pesquisando e adicionando faixas à playlist
for artista in artistas:
    resultados = sp.search(q='artist:' + artista, type='artist', limit=1)
    if len(resultados['artists']['items']) > 0:
        artista_id = resultados['artists']['items'][0]['id']
        top_musicas = sp.artist_top_tracks(artista_id)
        for faixa in top_musicas['tracks'][:10]:
            sp.playlist_add_items(playlist_id, [faixa['uri']])

# Obtendo o link da playlist
playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
print("Link da playlist:", playlist_url)
