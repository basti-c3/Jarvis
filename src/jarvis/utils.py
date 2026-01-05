import sounddevice as sd
import soundfile as sf


def play_audio_file(file_path):
    data, samplerate = sf.read(file_path, dtype='float32')
    sd.play(data, samplerate)
    sd.wait()  # Wait until playback is done
