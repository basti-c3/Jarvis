import sounddevice as sd
import soundfile as sf


def play_audio_file(file_path):
    data, samplerate = sf.read(file_path, dtype='float32')
    sd.play(data, samplerate)
    sd.wait()  # Wait until playback is done


def find_anker_usb_mic(name_substring="Anker"):
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0 and name_substring.lower() in dev['name'].lower():
            return i, dev['default_samplerate']
    return None, None
