import numpy as np
import zmq

from shared.ipc import client
from jarvis.core.exceptions import QuitJarvis
from shared.Jarvis import jarvis
from shared.utils import Warn, STOP_SIGNAL


def transcribe_command(audio_buffer: np.ndarray):
    """
        Send full command audio to STT service and return text
    """
    stt_service_client = client("tcp://127.0.0.1:5555", stream_pattern=zmq.REQ)
    try:
        stt_service_client.setsockopt(zmq.RCVTIMEO, 3000)
        stt_service_client.send(audio_buffer.tobytes())
        return_text = stt_service_client.recv_string()
        if STOP_SIGNAL in return_text:
            raise QuitJarvis()
        return return_text
    except zmq.error.Again:  # timeout exception
        # Log a specific error message
        Warn("ERROR: Speech to text service did not respond within timeout!")
        jarvis.reset_stt_service_client()
        jarvis.say("Sorry Sir, but the speech service is not responding.")
    finally:
        stt_service_client.close()