import threading
import sounddevice as sd

from jarvis.core.audio_callback import audio_callback
from jarvis.core.process_audio import continuous_processing
from shared.stop_event import stop_event
from shared import stt_config as config


def run_recognition(command: str = None):
    """Run continuous recognition. Optionally feed a test command for dev/test mode."""

    recognition_thread = threading.Thread(
        target=continuous_processing,
        args=(command,),
        daemon=True
    )
    recognition_thread.start()

    try:
        with sd.InputStream(
            samplerate=config.AUDIO_RATE,
            channels=config.CHANNELS,
            dtype='int16',
            callback=audio_callback,
            blocksize=int(config.BUFFER_DURATION * config.AUDIO_RATE),
        ):
            stop_event.wait()
    except KeyboardInterrupt:
        print("Stopping...")
        stop_event.set()
    finally:
        print("Exiting core program.")
