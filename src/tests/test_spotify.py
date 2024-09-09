import unittest

from src.spotify.SpotifyCommand import SpotifyCommand


class TestSpotifyCommand(unittest.TestCase):

    def test_preprocessing_command(self):
        spotify_command = SpotifyCommand("Play the Lazy Song from Spotify")
        self.assertEqual(spotify_command.search_str, 'the lazy song')

        spotify_command = SpotifyCommand("Play the Lazy Song")
        self.assertEqual(spotify_command.search_str, 'the lazy song')

        spotify_command = SpotifyCommand("Play a moody playlist")
        self.assertEqual(spotify_command.search_str, 'moody')

        spotify_command = SpotifyCommand("Play my moody playlist")
        self.assertEqual(spotify_command.search_str, 'moody')

        spotify_command = SpotifyCommand("Play moody playlist")
        self.assertEqual(spotify_command.search_str, 'moody')

    def test_track_search(self):
        spotify_command = SpotifyCommand("Play the Lazy Song")
        self.assertEqual(spotify_command.type, 'track')
        self.assertEqual(spotify_command.search_str, 'the lazy song')

        spotify_command = SpotifyCommand("Play the Lazy Song from Bruno Mars")
        self.assertEqual(spotify_command.type, 'track')
        self.assertEqual(spotify_command.search_str, 'the lazy song')
        self.assertEqual(spotify_command.artist_str, 'bruno mars')

        spotify_command = SpotifyCommand("Play the Lazy Song from Bruno Mars from Spotify")
        self.assertEqual(spotify_command.type, 'track')
        self.assertEqual(spotify_command.search_str, 'the lazy song')
        self.assertEqual(spotify_command.artist_str, 'bruno mars')

        spotify_command = SpotifyCommand("Play track Me Enamoré from Shakira")
        self.assertEqual(spotify_command.type, 'track')
        self.assertEqual(spotify_command.search_str, 'me enamoré')
        self.assertEqual(spotify_command.artist_str, 'shakira')

        spotify_command = SpotifyCommand("Play the amazing song The Lazy Song from Bruno Mars")
        self.assertEqual(spotify_command.type, 'track')
        self.assertEqual(spotify_command.search_str, 'the lazy song')

        spotify_command = SpotifyCommand("Play the great track The Lazy Song from Bruno Mars")
        self.assertEqual(spotify_command.type, 'track')
        self.assertEqual(spotify_command.search_str, 'the lazy song')

        spotify_command = SpotifyCommand("Play chilling music from Shakira")
        self.assertEqual(spotify_command.type, 'track')  # This should be a track search, not a playlist search
        self.assertEqual(spotify_command.search_str, 'chilling music')
        self.assertEqual(spotify_command.artist_str, 'shakira')

    def test_album_search(self):
        spotify_command = SpotifyCommand("Play album El Dorado")
        self.assertEqual(spotify_command.type, 'album')
        self.assertEqual(spotify_command.search_str, 'el dorado')

        spotify_command = SpotifyCommand("Play the album El Dorado from Shakira")
        self.assertEqual(spotify_command.type, 'album')
        self.assertEqual(spotify_command.search_str, 'el dorado')
        self.assertEqual(spotify_command.artist_str, 'shakira')

    def test_artist_search(self):
        spotify_command = SpotifyCommand("Play something from Adele")
        self.assertEqual(spotify_command.type, 'artist')
        self.assertEqual(spotify_command.search_str, 'adele')
        self.assertEqual(spotify_command.artist_str, 'adele')

        spotify_command = SpotifyCommand("Play some songs from Adele")
        self.assertEqual(spotify_command.type, 'artist')
        self.assertEqual(spotify_command.search_str, 'adele')
        self.assertEqual(spotify_command.artist_str, 'adele')

        spotify_command = SpotifyCommand("Play some music from Adele")
        self.assertEqual(spotify_command.type, 'artist')
        self.assertEqual(spotify_command.search_str, 'adele')
        self.assertEqual(spotify_command.artist_str, 'adele')

        spotify_command = SpotifyCommand("Play music from Adele")
        self.assertEqual(spotify_command.type, 'artist')
        self.assertEqual(spotify_command.search_str, 'adele')
        self.assertEqual(spotify_command.artist_str, 'adele')

        spotify_command = SpotifyCommand("Play artist Adele")
        self.assertEqual(spotify_command.type, 'artist')
        self.assertEqual(spotify_command.search_str, 'adele')
        self.assertEqual(spotify_command.artist_str, 'adele')

    def test_playlist_search(self):
        spotify_command = SpotifyCommand("Play playlist rock music")
        self.assertEqual(spotify_command.type, 'playlist')
        self.assertEqual(spotify_command.search_str, 'rock music')

        spotify_command = SpotifyCommand("Play the playlist rock music")
        self.assertEqual(spotify_command.type, 'playlist')
        self.assertEqual(spotify_command.search_str, 'rock music')

        spotify_command = SpotifyCommand("Play a rock music playlist")
        self.assertEqual(spotify_command.type, 'playlist')
        self.assertEqual(spotify_command.search_str, 'rock music')

        spotify_command = SpotifyCommand("Play my rock music playlist")
        self.assertEqual(spotify_command.type, 'playlist')
        self.assertEqual(spotify_command.search_str, 'rock music')

        spotify_command = SpotifyCommand("Play the rock music playlist")
        self.assertEqual(spotify_command.type, 'playlist')
        self.assertEqual(spotify_command.search_str, 'the rock music')  # watch out

        spotify_command = SpotifyCommand("Play some chilling music")
        self.assertEqual(spotify_command.type, 'playlist')
        self.assertEqual(spotify_command.search_str, 'chilling')

        spotify_command = SpotifyCommand("Play chilling music")
        self.assertEqual(spotify_command.type, 'playlist')
        self.assertEqual(spotify_command.search_str, 'chilling')


if __name__ == '__main__':
    unittest.main()
