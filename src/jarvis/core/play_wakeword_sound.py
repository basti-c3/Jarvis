import sounddevice as sd
import soundfile as sf
import threading


def play_wakeword_sound(file_path: str):
    """
    Plays a wakeword WAV file asynchronously using sounddevice.
    """

    def _play():
        data, samplerate = sf.read(file_path, dtype='float32')
        sd.play(data, samplerate)
        sd.wait()  # Wait until playback is done

    # Run in a separate thread so it doesn't block your main loop
    threading.Thread(target=_play, daemon=True).start()
