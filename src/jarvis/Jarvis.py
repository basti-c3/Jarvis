import zmq

from shared.global_init import tts_service_client
from shared.utils import Warn


class Jarvis:
    processing = False

    def say(self, text: str):
        try:
            tts_service_client.send_string(text)
            tts_service_client.recv()
        except zmq.error.Again:  # timeout exception
            # Log a specific error message
            Warn("ERROR in TTS: Speech to text service did not respond within timeout!")


jarvis = Jarvis()
