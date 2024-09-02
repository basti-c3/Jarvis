import queue
from src.spotify.SpotifyAPI import SpotifyAPI

# Queue to communicate between recording and recognition threads
audio_queue = queue.Queue()
spotify = SpotifyAPI()

