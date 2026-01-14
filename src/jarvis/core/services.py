import zmq
from shared.ipc import client

from shared.utils import STOP_SIGNAL
from jarvis.core.exceptions import QuitJarvis, SttServiceError, TtsServiceError


def send_stt_service(msg=None, stop=False):
    if stop:
        msg = STOP_SIGNAL.encode("utf-8")

    stt_service_client = client("tcp://127.0.0.1:5555", stream_pattern=zmq.REQ)
    try:
        stt_service_client.setsockopt(zmq.RCVTIMEO, 3000)
        stt_service_client.send(msg)

        if not stop:
            return_text = stt_service_client.recv_string()
            if STOP_SIGNAL in return_text:
                raise QuitJarvis()
            return return_text
    except zmq.error.Again:  # timeout exception
        raise SttServiceError("ERROR: Speech to text service did not respond within timeout!")
    finally:
        stt_service_client.close()


def send_tts_service(msg=None, stop=False):
    if stop:
        msg = STOP_SIGNAL
    tts_service_client = client("tcp://127.0.0.1:5556", stream_pattern=zmq.REQ)
    try:
        tts_service_client.setsockopt(zmq.RCVTIMEO, 3000)
        tts_service_client.send_string(msg)
        tts_service_client.recv()  # No return required, so don't do anything with it
    except zmq.error.Again:  # timeout exception
        # Log a specific error message
        raise TtsServiceError("ERROR in TTS: Speech to text service did not respond within timeout!")
    finally:
        tts_service_client.close()
