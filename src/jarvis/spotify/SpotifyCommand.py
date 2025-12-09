from spotify.PlayType import play_types
from spotify.SpotifyService import SpotifyService
from spotify.spotify_utils import *


class SpotifyCommand:
    def __init__(self, command_str):
        self.spotify_service = SpotifyService()
        self.artist_split_words = ['by', 'from']
        self.command_str = command_str.lower()
        self.type = None  # Is set in the extract method
        self.search_str = None  # Is set in the extract method
        self.artist_str = None  # Is set in the extract method
        self.extract()

    def extract(self):
        search_str = preprocess_spotify_search_string(self.command_str)  # For example "hello from adele"

        if any(word in search_str for word in self.artist_split_words):  # 'from spotify' would be removed already
            search_str, artist_str = extract_artist_from_search_string(search_str, self.artist_split_words)
            # "hello from adele" --> ["hello", "adele"]
            self.search_str = search_str
            self.artist_str = artist_str

        if self.artist_str is not None and (
                search_str == 'something' or search_str == 'some music' or search_str == 'music' or
                search_str == 'some songs' or search_str == 'songs' or search_str == 'song' or
                search_str == 'some song'):
            self.type = play_types.artist
            search_str = self.artist_str
        elif 'playlist ' in search_str.strip():  # "play playlist rock music"
            search_str = search_str.split('playlist ', 1)[1]
            self.type = play_types.playlist
        elif ' playlist' in search_str:  # "play a rock music playlist"
            search_str = search_str.split(' playlist', 1)[0]
            self.type = play_types.playlist
        elif 'album ' in search_str:
            search_str = search_str.split('album ', 1)[1]
            self.type = play_types.album
        elif 'artist ' in search_str:  # remove artist from query and search for artists
            search_str = search_str.split('artist ', 1)[1]
            self.artist_str = search_str
            self.type = play_types.artist
        elif ' music' in search_str and self.artist_str is None:
            search_str = search_str.replace('some', '')
            search_str = search_str.split(' music', 1)[0]  # "some chilling music" --> "chilling" (playlist search)
            self.type = play_types.playlist
        elif 'song ' in search_str:
            search_str = search_str.split('song ', 1)[1]
            self.type = play_types.track
        elif 'track ' in search_str:
            search_str = search_str.split('track ', 1)[1]
            self.type = play_types.track
        else:
            # Default search for tracks
            self.type = play_types.track

        self.search_str = normalize_whitespacing(search_str)  # To remove possible double spaces

    def execute(self):
        if self.search_str is None:
            jarvis.say("Sorry Sir, I did not get that, would you mind repeating that, please?")
            raise Exception("Error in SpotifyCommand: search_str is None when executing!")

        if self.type == play_types.track:
            self.spotify_service.play_track(self.search_str, self.artist_str)
        elif self.type == play_types.artist:
            self.spotify_service.play_artist(self.search_str)
        elif self.type == play_types.album:
            self.spotify_service.play_album(self.search_str, self.artist_str)
        elif self.type == play_types.playlist:
            self.spotify_service.play_playlist(self.search_str)
        else:
            # jarvis.say(f"Sorry Sir, but I do not know how to play something called {self.type}.")
            jarvis.say(f"Sorry Sir, but I did not understand what you want me to play.")
            raise Exception(f"Error in SpotifyCommand in execute: self.type = {self.type} is unknown!")
