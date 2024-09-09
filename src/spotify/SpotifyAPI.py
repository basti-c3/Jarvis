import json
import os
import urllib.parse
from datetime import datetime, timedelta

import requests
import base64
from dotenv import load_dotenv

from src.utils import spotify_base_url, spotify_token_url, spotify_auth_url, \
    spotify_redirect_url
from src.utils import Warn


class SpotifyAPI:
    def __init__(self):
        self.base_url = spotify_base_url
        self.token_url = spotify_token_url
        self.redirect_url = spotify_redirect_url
        self.token_dir_path = "../tokens/spotify"
        if not os.path.exists(self.token_dir_path):
            Warn(f"Error: path does not exist: {os.path.abspath(self.token_dir_path)}")
        self.token_date_format = "%Y-%m-%d_%H-%M-%S"

        # Load environment variables from .env file
        load_dotenv()
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        if not self.client_id or not self.client_secret:
            raise ValueError(f"Error in SpotifyAPI __init__: client_id: {self.client_id} and "
                             f"client_secret: {self.client_secret} must be set")

        # Load access token
        self.refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')
        if self.refresh_token is None or self.refresh_token == "":
            self.initialize_authorization_for_acccount_once()
        self._access_token_dict = None  # placeholder

    def connect_device(self):
        # Select the given device
        devices = self.get_available_devices()
        if devices:
            self.device_id = devices[0]['id']  # Choose the first available device
        else:
            raise Exception("Error in SpotifyAPI __init__: No devices found to play at!")

    def initialize_authorization_for_acccount_once(self):
        scope = 'user-read-playback-state user-modify-playback-state'
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_url,
            'scope': scope
        }

        url = f"{spotify_auth_url}?{urllib.parse.urlencode(params)}"
        raise Exception(f"No Error, just initialization: Visit the following URL ({url}) to authorize.\n"
                        f"      Then when accepting the connection, copy the code in the url and run "
                        f"      get_refresh_token_from_authorization with the given code to retrieve the needed "
                        f"      refresh_token. "
                        f"       For example \"{self.redirect_url}?code=ABC\" --> AUTHORIZATION_CODE=ABC"
                        "")

    def get_access_token(self):
        """Get a new access token if needed."""
        access_token_dict = self._access_token_dict  # Might be None

        if access_token_dict is None:
            self.load_saved_token()
            access_token_dict = self._access_token_dict  # Might still be None or expired

        # Check if the current access token is expired or about to expire
        current_time = datetime.now()
        expiring_time = datetime.strptime(access_token_dict.get('expires_at', current_time),
                                          self.token_date_format) if access_token_dict is not None else None
        if access_token_dict is None or expiring_time <= current_time:
            print("Access token is None, expired or about to expire. Refreshing...")
            self.refresh_access_token()
            access_token_dict = self._access_token_dict

        return access_token_dict.get('access_token')

    def load_saved_token(self):
        now = datetime.now()
        for filename in os.listdir(self.token_dir_path):
            if filename.startswith("spotify_access_token-") and filename.endswith(".json"):
                # Extract date from filename
                date_str = filename[len("spotify_access_token-"): -len(".json")]
                try:
                    file_date = datetime.strptime(date_str, self.token_date_format)
                except ValueError:
                    Warn(f"Warning in Spotify.load_saved_token: Date format invalid, got {date_str}, expect isoformat")
                    continue

                # Check if the file is older than close to one hour (avoid overlap at the edge)
                if now - file_date >= timedelta(minutes=59):
                    os.remove(os.path.join(self.token_dir_path, filename))
                else:
                    # Read the file into a dictionary
                    with open(os.path.join(self.token_dir_path, filename), 'r') as file:
                        data = json.load(file)
                    self._access_token_dict = data
                    return

    def save_token(self):
        if self._access_token_dict is None:
            raise Exception("Error in Spotify.save_token: self._access_token_dict is None but cannot be at this point")
        current_time = datetime.now()
        # Create a timestamp in ISO format
        timestamp = current_time.strftime(self.token_date_format)

        # Construct the filename
        filename = f"spotify_access_token-{timestamp}.json"
        file_path = os.path.join(self.token_dir_path, filename)

        # Ensure the directory exists
        os.makedirs(self.token_dir_path, exist_ok=True)

        # Remove old tokens
        for filename in os.listdir(self.token_dir_path):
            if filename.startswith("spotify_access_token-") and filename.endswith(".json"):
                os.remove(os.path.join(self.token_dir_path, filename))

        # Add the time point of the token expiring
        self._access_token_dict['expires_at'] = (
                current_time + timedelta(seconds=self._access_token_dict['expires_in'])
        ).strftime(self.token_date_format)

        # Save the new token to a JSON file
        with open(file_path, 'w') as file:
            json.dump(self._access_token_dict, file, indent=4)

    def refresh_access_token(self):
        if self.refresh_token is None or self.refresh_token == "":
            raise Exception("Error in get_access_token: self.refresh_token is not given but has to be at this point!")

        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

        request_data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        request_headers = {
            "Authorization": f"Basic {client_creds_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(self.token_url, headers=request_headers, data=request_data)

        if response.status_code == 200:
            self._access_token_dict = response.json()
            self.save_token()
        else:
            raise Exception(f"Error refreshing access token: {response.json()}")

    def get_headers(self):
        """Generate headers for Spotify API requests using the access token."""
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Spotify access token is None. Pleases obtain the token first")
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def get_top_tracks(self, artist_id):
        """Get the top tracks for an artist using their Spotify ID."""
        url = f"{self.base_url}/artists/{artist_id}/top-tracks"
        return self.get_tracks_by_query(url, "tracks")

    def get_album_tracks(self, album_id):
        """Get all tracks for an album using its Spotify ID."""
        url = f"{self.base_url}/albums/{album_id}/tracks"
        return self.get_tracks_by_query(url)

    def get_playlist_tracks(self, playlist_id):
        """Get all tracks for a playlist using its Spotify ID."""
        url = f"{self.base_url}/playlists/{playlist_id}/tracks"
        return self.get_tracks_by_query(url)

    def get_tracks_by_query(self, url, results_key='items'):
        headers = self.get_headers()
        params = {
            "market": "DE"  # Adjust market if needed
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()
            tracks = results.get(results_key, [])  # Use 'items' for the list of tracks
            return tracks
        else:
            Warn(f"Failed to get tracks for url {url}: {response.status_code}")
            return None

    def get_available_devices(self):
        """Retrieve a list of available Spotify Connect devices."""
        url = f"{self.base_url}/me/player/devices"
        headers = self.get_headers()
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            devices = response.json().get('devices', [])
            print("Found available devices:")
            for device in devices:
                print(
                    f" - {device['name']} (ID: {device['id']}) - Type: {device['type']}, Active: {device['is_active']}")
            return devices
        else:
            Warn(f"Spotify: Failed to get available devices, status: {response.status_code}")
            try:
                Warn(response.json())
            except Exception:  # If not possible to convert response to json, don't print it
                pass
            return None

    def transfer_playback(self):
        """Transfer playback to a specific device."""
        url = f"{self.base_url}/me/player"
        headers = self.get_headers()
        data = {
            "device_ids": [self.device_id],
            "play": True
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 204:
            print(f"Playback transferred to device ID: {self.device_id}")
        else:
            Warn(f"Spotify: Failed to transfer playback, status: {response.status_code}, {response.json()}")

    def play_track_uris(self, track_uris, shuffle=True):
        """Play a list of track URIs on a specific device."""
        url = f"{self.base_url}/me/player/play"
        headers = self.get_headers()

        url += f"?device_id={self.device_id}"

        # Set shuffle state if specified
        if shuffle:
            shuffle_url = f"{self.base_url}/me/player/shuffle?state=true&device_id={self.device_id}"
            shuffle_response = requests.put(shuffle_url, headers=headers)
            if shuffle_response.status_code != 200:
                Warn(f"Failed to set shuffle, status: {shuffle_response.status_code}")
                try:
                    Warn({shuffle_response.json()})
                except Exception:
                    pass

        # Make the request
        response = requests.put(url, headers=headers, json={"uris": track_uris})

        if response.status_code == 204:
            print("Playing tracks...")
        else:
            Warn(f"Spotify: Failed to play tracks, status: {response.status_code}, {response.json()}")

    def play_artist(self, artist_name):
        """Play an artist's top tracks."""
        # Search for the artist to get their Spotify ID
        artist_id = self.search_artist(artist_name)
        if not artist_id:
            Warn(f"Cannot play artist: '{artist_name}' not found.")
            return

        # Get the artist's top tracks
        top_tracks = self.get_top_tracks(artist_id)

        if not top_tracks:
            Warn(f"No top tracks found for artist with ID {artist_id}.")
            return

        # Playing tracks on specified device or default one
        top_tracks_uris = [track['uri'] for track in top_tracks]
        self.play_track_uris(top_tracks_uris, shuffle=True)

    def play_track(self, track_name, artist_name=None):
        """Play a song, optionally by a given artist."""
        if artist_name is not None:
            query_str = f"track:{track_name} artist:{artist_name}"
        else:
            query_str = track_name
        track = self.search_track(query_str)
        if not track:
            Warn(f"Cannot play song: '{track_name}' not found.")
            return
        self.play_track_uris([track['uri']], shuffle=False)

    def play_album(self, album_name, artist_name=None):
        """Play an album."""
        # Search for the album to get its Spotify ID
        album_id = self.search_album(album_name, artist_name)
        if not album_id:
            Warn(f"Cannot play album, got no id for '{album_name}'.")
            return

        # Get the album tracks
        album_tracks = self.get_album_tracks(album_id)
        if not album_tracks:
            Warn(f"No album tracks found for album with ID {album_id}.")
            return

        album_track_uris = [track['uri'] for track in album_tracks]
        self.play_track_uris(album_track_uris, shuffle=False)

    def play_playlist(self, playlist_name, artist_name=None):
        """Play a playlist, both your own or public ones possible."""
        playlist_id = self.search_playlist(playlist_name, artist_name)
        if not playlist_id:
            Warn(f"Cannot play playlist, got no id for '{playlist_id}'.")
            return

        # Get the playlist tracks
        playlist_items = self.get_playlist_tracks(playlist_id)
        if not playlist_items:
            Warn(f"No playlist tracks found for playlist with ID {playlist_id}.")
            return
        playlist_track_uris = [item['track']['uri'] for item in playlist_items if 'track' in item]
        self.play_track_uris(playlist_track_uris, shuffle=True)

    def search(self, query, types='track,artist,album,playlist', limit=10):
        """Search for content on Spotify across multiple types."""
        url = f"{self.base_url}/search"
        headers = self.get_headers()
        params = {
            'q': query,
            'type': types,
            'limit': limit
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()
            return results
        else:
            Warn(f"Spotify: Search failed for url {url}, status: {response.status_code}")
            return None

    def search_track(self, query_str):
        """Search for a song by name and return its Spotify ID."""
        results = self.search(query_str, types="track")
        if results is not None:
            items = results.get('tracks', {}).get('items', [])
            if items:
                track = items[0]
                return track
            else:
                print(f"No track found with the name '{query_str}'")
                return None
        return None

    def search_artist(self, artist_name):
        """Search for an artist by name and return their Spotify ID."""
        results = self.search(artist_name, types="artist")
        if results is not None:
            items = results.get('artists', {}).get('items', [])
            if items:
                artist_id = items[0]['id']
                return artist_id
            else:
                Warn(f"No artist found with the name '{artist_name}'")
                return None
        return None

    def search_album(self, album_name, artist_name=None):
        """Search for an album by name and return its Spotify ID."""
        if artist_name is not None:
            query_str = f'artist:"{artist_name}" album:"{album_name}"'
        else:
            query_str = album_name

        results = self.search(query_str, types="album")
        if results is not None:
            items = results.get('albums', {}).get('items', [])
            if items:
                album_id = items[0]['id']
                return album_id
            else:
                print(f"No album found with the name '{album_name}'")
                return None
        return None

    def search_playlist(self, playlist_name, artist_name=None):
        """Search for a playlist by name and return its Spotify ID."""
        if artist_name is not None:
            query_str = f'artist:"{artist_name}" track:"{playlist_name}"'
            types = "track"  # When given artist_name as well ("some chilly music from Shakira"), search for tracks
        else:
            query_str = playlist_name
            types = "playlist"

        results = self.search(query_str, types=types)
        if results is not None:
            items = results.get('playlists', {}).get('items', [])
            if items:
                playlist_id = items[0]['id']
                return playlist_id
            else:
                Warn(f"No playlist found with the name '{playlist_name}'")
                return None
        return None
