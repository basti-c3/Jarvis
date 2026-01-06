import threading
import sounddevice as sd

from jarvis.core.audio_callback import audio_callback
from jarvis.core.process_audio import continuous_processing
from shared.stop_event import stop_event
from shared import stt_config as config
from shared.utils import Warn
from shared.Jarvis import jarvis


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
                device=jarvis.anker_mic_device,
                samplerate=jarvis.audio_mic_sample_rate,
                channels=config.CHANNELS,
                dtype='int16',
                callback=audio_callback,
                blocksize=int(config.BUFFER_DURATION * jarvis.audio_mic_sample_rate),
        ):
            stop_event.wait()
    except KeyboardInterrupt:
        print("Stopping...")
        stop_event.set()
    except sd.PortAudioError:
        Warn("Something went wrong with the audio port. Are you sure you plugged in into the configured port?")
    finally:
        print("Exiting core program.")
