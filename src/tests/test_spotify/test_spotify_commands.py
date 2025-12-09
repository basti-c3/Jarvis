import pytest
from spotify.SpotifyCommand import SpotifyCommand


class TestSpotifyCommand:
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
    def test_preprocessing_command(self, input_command, expected_search_str):
        spotify_command = SpotifyCommand(command_str=input_command)
        assert spotify_command.search_str == expected_search_str

    @pytest.mark.parametrize(
        "input_command, expected_type, expected_search, expected_artist",
        [
            # Track searches
            ("Play the Lazy Song", "track", "the lazy song", None),
            ("Play the Lazy Song from Bruno Mars", "track", "the lazy song", "bruno mars"),
            ("Play the Lazy Song from Bruno Mars from Spotify", "track", "the lazy song", "bruno mars"),
            ("Play track Me Enamoré from Shakira", "track", "me enamoré", "shakira"),
            ("Play the amazing song The Lazy Song from Bruno Mars", "track", "the lazy song", "bruno mars"),
            ("Play the great track The Lazy Song from Bruno Mars", "track", "the lazy song", "bruno mars"),
            ("Play chilling music from Shakira", "track", "chilling music", "shakira"),
            ("play by myself by linkin park", "track", "by myself", "linkin park"),
            ("play all by myself by celine dion", "track", "all by myself", "celine dion"),
            ("play girl from the north country by bob dylan", "track", "girl from the north country", "bob dylan"),

            # Album searches
            ("Play album El Dorado", "album", "el dorado", None),
            ("Play the album El Dorado from Shakira", "album", "el dorado", "shakira"),

            # Artist searches
            ("Play something from Adele", "artist", "adele", "adele"),
            ("Play some songs from Adele", "artist", "adele", "adele"),
            ("Play some music from Adele", "artist", "adele", "adele"),
            ("Play music from Adele", "artist", "adele", "adele"),
            ("Play artist Adele", "artist", "adele", "adele"),

            # Playlist searches
            ("Play playlist rock music", "playlist", "rock music", None),
            ("Play the playlist rock music", "playlist", "rock music", None),
            ("Play a rock music playlist", "playlist", "rock music", None),
            ("Play my rock music playlist", "playlist", "rock music", None),
            ("Play the rock music playlist", "playlist", "the rock music", None),
            ("Play some chilling music", "playlist", "chilling", None),
            ("Play chilling music", "playlist", "chilling", None),
        ]
    )
    def test_spotify_command_types(self, input_command, expected_type, expected_search, expected_artist):
        spotify_command = SpotifyCommand(command_str=input_command)
        assert spotify_command.type == expected_type
        assert spotify_command.search_str == expected_search
        assert spotify_command.artist_str == expected_artist
