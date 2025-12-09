from requests import Response

from Jarvis import jarvis
from spotify.PlayType import play_types
from spotify.SpotifyApiCommunicationService import SpotifyApiCommunicationService
from spotify.spotify_utils import raise_spotify_error
from utils import *


class SpotifyService:
    def __init__(self):
        self.spotify_api = SpotifyApiCommunicationService()

    def play_artist(self, artist_name):
        """Play an artist's top tracks."""
        # Search for the artist to get their Spotify ID
        artist_id = self.spotify_api.search_artist(artist_name)
        if not artist_id:
            jarvis.say(f"Sorry, but I did not find artist {artist_name}.")
            Warn(f"Cannot play artist: '{artist_name}' not found.")
            return

        # Get the artist's top tracks
        top_tracks = self.spotify_api.get_top_tracks(artist_id)

        if not top_tracks:
            jarvis.say(f"Sorry, but I did not find the top tracks by artist {artist_name}.")
            Warn(f"No top tracks found for artist with ID {artist_id}.")
            return

        # Playing tracks on specified device or default one
        top_tracks_uris = [track['uri'] for track in top_tracks]
        self._play(top_tracks_uris, play_types.artist, artist_name, shuffle=True)

    def play_track(self, track_name, artist_name=None):
        """Play a song, optionally by a given artist."""
        if artist_name is not None:
            query_str = f"track:{track_name} artist:{artist_name}"
        else:
            query_str = track_name

        play_content_str = f"{track_name} by {artist_name}" if artist_name else track_name

        track = self.spotify_api.search_track(query_str)
        if not track:
            Warn(f"Cannot play song: '{track_name}' not found.")
            jarvis.say(f"Sorry, but I did not find the song {play_content_str}.")
            return

        self._play([track['uri']], play_types.track, play_content_str, shuffle=False)

    def play_album(self, album_name, artist_name=None):
        """Play an album."""
        play_content_str = f'{album_name} by {artist_name}' if artist_name else album_name

        # Search for the album to get its Spotify ID
        album_id = self.spotify_api.search_album(album_name, artist_name)
        if not album_id:
            Warn(f"Cannot play album, got no id for '{album_name}'.")
            jarvis.say(f"Sorry, but I did not find the album {play_content_str}.")
            return

        # Get the album tracks
        album_tracks = self.spotify_api.get_album_tracks(album_id)
        if not album_tracks:
            Warn(f"No album tracks found for album with ID {album_id}.")
            jarvis.say(f"Sorry, but I did not find any tracks for album {play_content_str}.")
            return

        album_track_uris = [track['uri'] for track in album_tracks]

        self._play(album_track_uris, play_types.album, play_content_str, shuffle=False)

    def play_playlist(self, playlist_name, artist_name=None):
        """Play a playlist, both your own or public ones possible."""
        play_content_str = f'{playlist_name} by {artist_name}' if artist_name else playlist_name

        playlist_id = self.spotify_api.search_playlist(playlist_name, artist_name)
        if not playlist_id:
            Warn(f"Cannot play playlist, got no id for '{playlist_id}'.")
            jarvis.say(f"Sorry, but I did not find the playlist {play_content_str}.")
            return

        # Get the playlist tracks
        playlist_items = self.spotify_api.get_playlist_tracks(playlist_id)
        if not playlist_items:
            Warn(f"No playlist tracks found for playlist with ID {playlist_id}.")
            jarvis.say(f"Sorry, but I did not find any tracks in playlist {play_content_str}.")
            return
        playlist_track_uris = [item['track']['uri'] for item in playlist_items if 'track' in item]

        self._play(playlist_track_uris, play_types.playlist, play_content_str, shuffle=True)

    def _play(self, track_uris, play_type, play_content_str, shuffle=True):
        """Send the play command."""
        try:
            self.spotify_api.play(track_uris, shuffle)
            jarvis.say(f'Playing {play_content_str} from Spotify.')
        except ConnectionError as error:
            error_response: Response = error.args[0]
            raise_spotify_error(f'{play_type} {play_content_str}', error_response.status_code, error_response.json())