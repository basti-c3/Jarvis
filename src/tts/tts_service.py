import zmq

from shared.ipc import server
from tts.utils import say
from shared.utils import STOP_SIGNAL

tts_service_server = server("tcp://127.0.0.1:5556", stream_pattern=zmq.REP)

while True:
    text_to_speak = tts_service_server.recv_string()
    if STOP_SIGNAL in text_to_speak:
        print("Received stop signal, exiting TTS loop")
        break

    say(text_to_speak)
    tts_service_server.send(b"OK")
