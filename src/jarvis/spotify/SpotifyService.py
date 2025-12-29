from Jarvis import jarvis
from spotify.SpotifyCommandTypes import PlayType
from spotify.SpotifyApiCommunicationService import SpotifyApiCommunicationService
from spotify.spotify_action import spotify_action
from shared.utils import *


class SpotifyService:
    def __init__(self):
        self.spotify_api = SpotifyApiCommunicationService()

    def play_artist(self, artist_name):
        """Play an artist's top tracks."""
        # Search for the artist to get their Spotify ID
        artist_id = self.spotify_api.search_artist(artist_name)
        if not artist_id:
            # jarvis.say(f"Sorry, but I did not find artist {artist_name}.")
            jarvis.say(f"Sorry Sir, but I did not find that artist.")
            Warn(f"Cannot play artist: '{artist_name}' not found.")
            return

        # Get the artist's top tracks
        top_tracks = self.spotify_api.get_top_tracks(artist_id)

        if not top_tracks:
            # jarvis.say(f"Sorry, but I did not find the top tracks by artist {artist_name}.")
            jarvis.say(f"Sorry, but I did not find the top tracks of that artist.")
            Warn(f"No top tracks found for artist with ID {artist_id}.")
            return

        # Playing tracks on specified device or default one
        top_tracks_uris = [track['uri'] for track in top_tracks]
        self._play(top_tracks_uris, PlayType.artist, artist_name, shuffle=True)

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
            # jarvis.say(f"Sorry, but I did not find the song {play_content_str}.")
            jarvis.say("Sorry Sir, but I could not find that song.")
            return

        self._play([track['uri']], PlayType.track, play_content_str, shuffle=False)

    def play_album(self, album_name, artist_name=None):
        """Play an album."""
        play_content_str = f'{album_name} by {artist_name}' if artist_name else album_name

        # Search for the album to get its Spotify ID
        album_id = self.spotify_api.search_album(album_name, artist_name)
        if not album_id:
            Warn(f"Cannot play album, got no id for '{album_name}'.")
            # jarvis.say(f"Sorry, but I did not find the album {play_content_str}.")
            jarvis.say("Sorry Sir, but I did not find that album by id.")
            return

        # Get the album tracks
        album_tracks = self.spotify_api.get_album_tracks(album_id)
        if not album_tracks:
            Warn(f"No album tracks found for album with ID {album_id}.")
            # jarvis.say(f"Sorry, but I did not find any tracks for album {play_content_str}.")
            jarvis.say("Sorry Sir, but I did not find that album.")
            return

        album_track_uris = [track['uri'] for track in album_tracks]

        self._play(album_track_uris, PlayType.album, play_content_str, shuffle=False)

    def play_playlist(self, playlist_name, artist_name=None):
        """Play a playlist, both your own or public ones possible."""
        play_content_str = f'{playlist_name} by {artist_name}' if artist_name else playlist_name

        playlist_id = self.spotify_api.search_playlist(playlist_name, artist_name)
        if not playlist_id:
            Warn(f"Cannot play playlist, got no id for '{playlist_id}'.")
            # jarvis.say(f"Sorry, but I did not find the playlist {play_content_str}.")
            jarvis.say("Sorry Sir, but I did not find that playlist.")
            return

        # Get the playlist tracks
        playlist_items = self.spotify_api.get_playlist_tracks(playlist_id)
        if not playlist_items:
            Warn(f"No playlist tracks found for playlist with ID {playlist_id}.")
            # jarvis.say(f"Sorry, but I did not find any tracks in playlist {play_content_str}.")
            jarvis.say(f"Sorry Sir, but I did not find any tracks in the given playlist.")
            return
        playlist_track_uris = [item['track']['uri'] for item in playlist_items if 'track' in item]

        self._play(playlist_track_uris, PlayType.playlist, play_content_str, shuffle=True)

    @spotify_action("Certainly, Sir. Playing from Spotify now!")
    def _play(self, track_uris, play_type, play_content_str, shuffle=True):
        """Send the play command."""
        self.spotify_api.play_tracks(track_uris, shuffle)

    @spotify_action("Of course, Sir!")
    def stop_playing(self):
        """Stop playing music."""
        self.spotify_api.stop()

    @spotify_action("Most certainly, Sir! Enjoy!")
    def continue_playing(self):
        self.spotify_api.play()

    @spotify_action("Alright, skipping the song!")
    def skip_song(self):
        self.spotify_api.skip()

    @spotify_action()
    def set_repeat_mode(self, on):
        self.spotify_api.repeat_mode(on)
        if on:
            jarvis.say("Alright, let's make an infinite loop of this song!")
        else:
            jarvis.say("Turning repeat mode off again.")
