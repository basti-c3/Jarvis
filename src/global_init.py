import queue
from src.spotify.SpotifyAPI import SpotifyAPI
from src.text_to_speech.JarvisTTS import JarvisTTS

# Queue to communicate between recording and recognition threads
audio_queue = queue.Queue()
spotify = SpotifyAPI()
spotify.connect_device()
# tts model
text_to_speech = JarvisTTS()
