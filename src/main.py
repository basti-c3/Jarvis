import threading
import sounddevice as sd
import audio.config as config
from audio.audio_listening import audio_callback
from audio.process_audio import process_audio

if __name__ == "__main__":
    # Create and start the recording thread
    recognition_thread = threading.Thread(target=process_audio)
    recognition_thread.daemon = True
    recognition_thread.start()

    try:
        with sd.InputStream(samplerate=config.AUDIO_RATE, channels=1, dtype='int16', callback=audio_callback,
                            blocksize=int(config.BUFFER_DURATION * config.AUDIO_RATE)):
            while True:
                pass  # Keep the main thread alive while vosk processing occurs in the background
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        print("Resources cleaned up. Exiting program.")
