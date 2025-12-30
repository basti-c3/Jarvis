import zmq

from shared.ipc import server
from stt.utils import get_command_text

stt_service_server = server("tcp://127.0.0.1:5555", stream_pattern=zmq.REP)

while True:
    audio_bytes = stt_service_server.recv()
    if not isinstance(audio_bytes, bytes):
        # Ensure right type before
        raise Exception(f"Error in speech_to_text service: Only takes audio bytes at this point, but got {type(audio_bytes)}")
    text = get_command_text(audio_bytes)
    print(f"reached here22! {text}")
    stt_service_server.send_string(text)
