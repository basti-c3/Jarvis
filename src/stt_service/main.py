import zmq

from shared.ipc import server
from stt_service.utils import get_command_text
from shared.utils import STOP_SIGNAL

stt_service_server = server("tcp://127.0.0.1:5555", stream_pattern=zmq.REP)

while True:
    msg_bytes = stt_service_server.recv()
    if not isinstance(msg_bytes, bytes):
        # Ensure right type before
        raise Exception(f"Error in speech_to_text service: Only takes audio bytes at this point, but got {type(msg_bytes)}")
    if STOP_SIGNAL.encode("utf-8") in msg_bytes:
        print("Received stop signal, exiting STT loop")
        break

    text = get_command_text(msg_bytes)
    stt_service_server.send_string(text)
