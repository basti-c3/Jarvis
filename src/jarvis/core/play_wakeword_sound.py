import threading

from jarvis.utils import play_audio_file
from shared.Jarvis import jarvis


def play_wakeword_sound(file_path: str):
    """
    Plays a wakeword WAV file asynchronously using sounddevice.
    """

    def _play():
        play_audio_file(file_path, jarvis.anker_speaker_device, jarvis.audio_speaker_sample_rate)

    # Run in a separate thread so it doesn't block your main loop
    threading.Thread(target=_play, daemon=True).start()
