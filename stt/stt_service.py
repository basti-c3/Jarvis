import numpy as np

from shared.ipc import server
from stt.utils import get_command_text

sock = server("tcp://127.0.0.1:5555")

while True:
    audio_bytes = sock.recv()
    if not isinstance(audio_bytes, bytes):
        # Ensure right type before
        raise Exception(f"Error in speech_to_text service: Only takes audio bytes at this point, but got {type(audio_bytes)}")
    text = get_command_text(audio_bytes)
    print("reached here22!")
    sock.send_string(text)
    print("reached here!")
