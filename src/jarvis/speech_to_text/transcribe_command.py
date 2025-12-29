import numpy as np
import zmq

from Jarvis import jarvis
from shared.global_init import stt_service
from shared.utils import Warn


def transcribe_command(audio_buffer: np.ndarray):
    """
        Send full command audio to STT service and return text
    """
    try:
        stt_service.send(audio_buffer.tobytes())
        return stt_service.recv_string()
    except zmq.error.Again:  # timeout exception
        # Log a specific error message
        Warn("ERROR: Speech to text service did not respond within timeout!")
        jarvis.say("Sorry Sir, but the speech service is not responding.")