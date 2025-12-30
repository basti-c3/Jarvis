from unittest.mock import patch

from core.process_command import process_command


class TestSpotifyBasicCommand:
    """Pytest-style tests for SpotifyCommand basic commands."""

    def test_stop_playing_track(self):
        """Tests that stop command trigger Spotify API call."""
        import spotify.SpotifyService as spotify_api
        # Get the method object directly from the class
        method_obj = spotify_api.SpotifyApiCommunicationService.stop
        with patch.object(spotify_api.SpotifyApiCommunicationService, method_obj.__name__) as mock_stop_track:
            process_command("Jarvis, stop playing music")
            mock_stop_track.assert_called_once_with()

    def test_skipping_track(self):
        """Tests that skip command trigger Spotify API call."""
        import spotify.SpotifyService as spotify_api
        # Get the method object directly from the class
        method_obj = spotify_api.SpotifyApiCommunicationService.skip
        with patch.object(spotify_api.SpotifyApiCommunicationService, method_obj.__name__) as mock_skip_track:
            process_command("Jarvis, skip this song, please")
            mock_skip_track.assert_called_once_with()
