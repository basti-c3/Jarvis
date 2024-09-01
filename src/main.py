import threading
import sounddevice as sd
import src.vosk_model.config as config
from src.vosk_model.audio_callback import audio_callback
from src.vosk_model.process_audio import continuous_processing

if __name__ == "__main__":
    # Create and start the recording thread
    recognition_thread = threading.Thread(target=continuous_processing)
    recognition_thread.daemon = True
    recognition_thread.start()

    try:
        with sd.InputStream(samplerate=config.AUDIO_RATE, channels=config.CHANNELS, dtype='int16',
                            callback=audio_callback, blocksize=int(config.BUFFER_DURATION * config.AUDIO_RATE)):
            while True:
                pass  # Keep the main thread alive while audio processing occurs in the background by process_audio
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        print("Resources cleaned up. Exiting program.")
