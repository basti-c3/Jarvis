import pytest
from jarvis.spotify.SpotifyCommand import SpotifyCommand
from jarvis.spotify.SpotifyCommandTypes import PlayType


class TestSpotifyPlayCommand:
    """Pytest-style tests for SpotifyCommand preprocessing and type detection."""

    @pytest.mark.parametrize(
        "input_command, expected_search_str",
        [
            ("Play the Lazy Song from Spotify", "the lazy song"),
            ("Play the Lazy Song", "the lazy song"),
            ("Play a moody playlist", "moody"),
            ("Play my moody playlist", "moody"),
            ("Play moody playlist", "moody"),
        ]
    )
    def test_spotify_command_extract(self, input_command, expected_search_str):
        spotify_command = SpotifyCommand(command_str=input_command)
        spotify_command.extract()
        assert spotify_command.search_str == expected_search_str

    @pytest.mark.parametrize(
        "input_command, expected_type, expected_search, expected_artist",
        [
            # Track searches
            ("Play the Lazy Song", PlayType.track, "the lazy song", None),
            ("Play the Lazy Song from Bruno Mars", PlayType.track, "the lazy song", "bruno mars"),
            ("Play the Lazy Song from Bruno Mars from Spotify", PlayType.track, "the lazy song", "bruno mars"),
            ("Play track Me Enamoré from Shakira", PlayType.track, "me enamoré", "shakira"),
            ("Play the amazing song The Lazy Song from Bruno Mars", PlayType.track, "the lazy song", "bruno mars"),
            ("Play the great track The Lazy Song from Bruno Mars", PlayType.track, "the lazy song", "bruno mars"),
            ("Play chilling music from Shakira", PlayType.track, "chilling music", "shakira"),
            ("play by myself by linkin park", PlayType.track, "by myself", "linkin park"),
            ("play all by myself by celine dion", PlayType.track, "all by myself", "celine dion"),
            ("play girl from the north country by bob dylan", PlayType.track, "girl from the north country", "bob dylan"),

            # Album searches
            ("Play album El Dorado", PlayType.album, "el dorado", None),
            ("Play the album El Dorado from Shakira", PlayType.album, "el dorado", "shakira"),

            # Artist searches
            ("Play something from Adele", PlayType.artist, "adele", "adele"),
            ("Play some songs from Adele", PlayType.artist, "adele", "adele"),
            ("Play some music from Adele", PlayType.artist, "adele", "adele"),
            ("Play music from Adele", PlayType.artist, "adele", "adele"),
            ("Play artist Adele", PlayType.artist, "adele", "adele"),

            # Playlist searches
            ("Play playlist rock music", PlayType.playlist, "rock music", None),
            ("Play the playlist rock music", PlayType.playlist, "rock music", None),
            ("Play a rock music playlist", PlayType.playlist, "rock music", None),
            ("Play my rock music playlist", PlayType.playlist, "rock music", None),
            ("Play the rock music playlist", PlayType.playlist, "the rock music", None),
            ("Play some chilling music", PlayType.playlist, "chilling", None),
            ("Play chilling music", PlayType.playlist, "chilling", None),
        ]
    )
    def test_spotify_command_types(self, input_command, expected_type, expected_search, expected_artist):
        spotify_command = SpotifyCommand(command_str=input_command)
        spotify_command.extract()
        assert spotify_command.type == expected_type
        assert spotify_command.search_str == expected_search
        assert spotify_command.artist_str == expected_artist
