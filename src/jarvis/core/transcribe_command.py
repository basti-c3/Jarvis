import numpy as np
import zmq

from shared.Jarvis import jarvis
from shared.utils import Warn


def transcribe_command(audio_buffer: np.ndarray):
    """
        Send full command audio to STT service and return text
    """
    try:
        jarvis.stt_service_client.send(audio_buffer.tobytes())
        return jarvis.stt_service_client.recv_string()
    except zmq.error.Again:  # timeout exception
        # Log a specific error message
        Warn("ERROR: Speech to text service did not respond within timeout!")
        jarvis.say("Sorry Sir, but the speech service is not responding.")