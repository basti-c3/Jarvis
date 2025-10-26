import queue

from vosk import KaldiRecognizer

from text_to_speech.JarvisTTS import JarvisTTS
from speech_to_text.JarvisSTT import JarvisSTT
from spotify.SpotifyService import SpotifyService

_spotify = None
_stt_model = None
_tts_model = None
_audio_queue = None


def init_globals():
    global _audio_queue
    global _spotify
    global _stt_model
    global _tts_model

    if _audio_queue is None:
        _audio_queue = queue.Queue()
    if _spotify is None:
        _spotify = SpotifyService()
        _spotify.connect_device()
    if _stt_model is None:
        _stt_model = JarvisSTT()
    if _tts_model is None:
        _tts_model = JarvisTTS()


def get_audio_queue():
    global _audio_queue
    if _audio_queue is None:
        _audio_queue = queue.Queue()
    return _audio_queue


def get_spotify_service() -> SpotifyService:
    global _spotify
    if _spotify is None:
        _spotify = SpotifyService()
        _spotify.connect_device()
    return _spotify


def get_stt_model() -> JarvisSTT:
    global _stt_model
    if _stt_model is None:
        _stt_model = JarvisSTT()
    return _stt_model


def get_stt_recognizer() -> KaldiRecognizer:
    global _stt_model
    if _stt_model is None:
        _stt_model = JarvisSTT()
    return _stt_model.recognizer


def get_tts_model() -> JarvisTTS:
    global _tts_model
    if _tts_model is None:
        _tts_model = JarvisTTS()
    return _tts_model
