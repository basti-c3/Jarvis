import zmq

from shared.global_init import tts_service
from shared.utils import Warn


class Jarvis:
    processing = False

    def say(self, text: str):
        try:
            tts_service.send_string(text)
            tts_service.recv()
        except zmq.error.Again:  # timeout exception
            # Log a specific error message
            Warn("ERROR in TTS: Speech to text service did not respond within timeout!")


jarvis = Jarvis()
