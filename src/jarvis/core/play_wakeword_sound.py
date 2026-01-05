import threading

from jarvis.utils import play_audio_file


def play_wakeword_sound(file_path: str):
    """
    Plays a wakeword WAV file asynchronously using sounddevice.
    """

    def _play():
        play_audio_file(file_path)

    # Run in a separate thread so it doesn't block your main loop
    threading.Thread(target=_play, daemon=True).start()
