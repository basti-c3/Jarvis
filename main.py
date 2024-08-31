import threading

from audio.audio_listening import record_audio
from audio.process_audio import process_audio

if __name__ == "__main__":
    # Create and start the recording thread
    record_thread = threading.Thread(target=record_audio)
    record_thread.daemon = True
    record_thread.start()

    # Run the processing and recognition in the main thread
    process_audio()
