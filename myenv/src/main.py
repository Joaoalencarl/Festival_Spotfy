from dotenv import load_dotenv
import os
from event_playlist_creator import EventPlaylistCreator

load_dotenv()

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
