import numpy as np
import pyaudio

from audio import config
from audio.global_vars import audio_queue


def record_audio():
    """Continuously record audio from the microphone and put it into a queue."""
    p = pyaudio.PyAudio()
    stream = p.open(format=config.FORMAT, channels=config.CHANNELS,
                    rate=config.RATE, input=True,
                    frames_per_buffer=config.CHUNK)

    print("Microphone is open and recording...")

    try:
        while True:
            # Read audio data from the microphone
            audio_data = stream.read(config.CHUNK, exception_on_overflow=False)

            # Convert audio data to numpy array and normalize
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # Put the audio data into the queue
            audio_queue.put(audio_array)

    except Exception as e:
        print(f"Error recording audio: {e}")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()