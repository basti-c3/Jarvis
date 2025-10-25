import threading
import sounddevice as sd
from speech_to_text import config
from speech_to_text.audio_callback import audio_callback
from speech_to_text.process_audio import continuous_processing


def run_recognition(command: str = None):
    """Run continuous recognition. Optionally feed a test command for dev/test mode."""

    recognition_thread = threading.Thread(target=continuous_processing, args=(command,))
    recognition_thread.daemon = True
    recognition_thread.start()

    try:
        with sd.InputStream(
            samplerate=config.AUDIO_RATE,
            channels=config.CHANNELS,
            dtype='int16',
            callback=audio_callback,
            blocksize=int(config.BUFFER_DURATION * config.AUDIO_RATE),
        ):
            while True:
                pass  # Keep main thread alive
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        print("Resources cleaned up. Exiting program.")
