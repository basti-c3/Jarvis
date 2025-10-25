import queue
from spotify.SpotifyAPI import SpotifyAPI
from text_to_speech.JarvisTTS import JarvisTTS
from speech_to_text.JarvisSTT import JarvisSTT

# Queue to communicate between recording and recognition threads
audio_queue = queue.Queue()
spotify = SpotifyAPI()
spotify.connect_device()
# stt model
stt_model: JarvisSTT = JarvisSTT()
# tts model
text_to_speech : JarvisTTS = JarvisTTS()
