from spotify_client import SpotifyClient


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
