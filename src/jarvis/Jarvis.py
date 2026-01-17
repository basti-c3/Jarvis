import zmq

from jarvis.utils import send_tts_service
from shared.utils import Warn


class Jarvis:
    def __init__(self):
        self._wake_word = None
        self._audio_queue = None

    @property
    def audio_queue(self):
        if self._audio_queue is None:
            from queue import Queue
            self._audio_queue = Queue()
        return self._audio_queue

    @property
    def wake_word(self):
        if self._wake_word is None:
            from jarvis.core.WakeWordEngine import WakeWordEngine
            self._wake_word = WakeWordEngine()
        return self._wake_word

    def say(self, text: str):
        try:
            send_tts_service(text)
        except zmq.error.Again:  # timeout exception
            # Log a specific error message
            Warn("ERROR in TTS: Speech to text service did not respond within timeout!")


jarvis = Jarvis()
