from unittest.mock import patch

from core.process_command import process_command


class TestProcessingCommand:
    """Tests for verifying song recognition and Spotify command handling."""

    def test_play_track_with_artist(self):
        """Tests that recognized play commands trigger Spotify API call."""
        import spotify.SpotifyService as spotify_api
        # Get the method object directly from the class
        method_obj = spotify_api.SpotifyService.play_track
        with patch.object(spotify_api.SpotifyService, method_obj.__name__) as mock_play_track:
            process_command("Jarvis, play waka waka from shakira")
            mock_play_track.assert_called_once_with("waka waka", "shakira")
