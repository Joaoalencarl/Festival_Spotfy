from playlist_manager import PlaylistManager


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
