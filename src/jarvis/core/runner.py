import threading
import traceback

import sounddevice as sd

from jarvis.core.audio_callback import audio_callback
from jarvis.core.process_audio import continuous_processing
from shared.stop_event import stop_event
from shared import stt_config as config
from shared.utils import Warn
from shared.Anker import anker


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
                device=anker.anker_mic_device,
                samplerate=anker.audio_mic_sample_rate,
                channels=config.CHANNELS,
                dtype='int16',  # Windows does not work with float32, it just silently doesnt call callback
                callback=audio_callback,
                blocksize=int(config.BUFFER_DURATION * anker.audio_mic_sample_rate),
        ):
            stop_event.wait()
    except KeyboardInterrupt:
        Warn("Stopping...")
        stop_event.set()
    except sd.PortAudioError as error:
        Warn("Something went wrong with the audio port. Are you sure you plugged in into the configured port?")
        Warn(error)
        Warn(traceback.format_exc())
    finally:
        Warn("Exiting core program.")
