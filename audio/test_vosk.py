import os
import threading
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Configuration Parameters
AUDIO_RATE = 16000  # Sample rate in Hz
BUFFER_DURATION = 0.5  # Duration of each buffer in seconds

# Initialize Vosk Model and Recognizer
model_path = "../models/vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print(f"Model path {model_path} not found. Please provide the correct model path.")
    exit(1)

model = Model(model_path)
recognizer = KaldiRecognizer(model, AUDIO_RATE)

# Queue to hold audio data for processing
audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    """Callback function for sounddevice to receive audio data."""
    if status:
        print(status, flush=True)
    # Convert audio data to bytes and put it in the queue
    audio_queue.put(indata.copy())


def recognize_audio_stream():
    """Thread function to recognize audio data from the stream in real-time."""
    while True:
        try:
            data = audio_queue.get(timeout=1)  # Get audio data from the queue
            if recognizer.AcceptWaveform(data.tobytes()):
                result = recognizer.Result()
                print(f"Full Result: {result}")
            else:
                partial_result = recognizer.PartialResult()
                print(f"Partial Result: {partial_result}")
        except queue.Empty:
            continue  # Continue if the queue is empty


# Start the audio recognition thread
recognition_thread = threading.Thread(target=recognize_audio_stream)
recognition_thread.daemon = True
recognition_thread.start()

print("Listening... Press Ctrl+C to stop.")

try:
    with sd.InputStream(samplerate=AUDIO_RATE, channels=1, dtype='int16', callback=audio_callback,
                        blocksize=int(BUFFER_DURATION * AUDIO_RATE)):
        while True:
            pass  # Keep the main thread alive while audio processing occurs in the background
except KeyboardInterrupt:
    print("Stopping...")
finally:
    print("Resources cleaned up. Exiting program.")
