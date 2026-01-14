import platform

import numpy as np
import soundfile as sf
import sounddevice as sd
from scipy.signal import resample_poly


def Warn(message, *args):
    # This prints a warning in red color into the terminal without breaking the code at the point of the warning
    if args:  # Checks if args is not empty
        print("\033[91m" + str(message) + " " + str(args) + "\033[0m")
    else:
        print("\033[91m" + str(message) + "\033[0m")


STOP_SIGNAL: str = "protocol suicide"


def find_anker_usb_mic(name_substring="Anker"):
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0 and name_substring.lower() in dev['name'].lower():
            return i, dev['default_samplerate']
    Warn("No Anker mic found! Is it plugged in?")
    # Check if running on Windows
    if platform.system() != "Windows":
        raise RuntimeError("This code only works on Windows. Detected OS: " + platform.system())
    return 1, 48000


def find_anker_usb_speaker(name_substring="Anker"):
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_output_channels'] > 0 and name_substring.lower() in dev['name'].lower():
            return i, dev['default_samplerate']
    Warn("No Anker speaker found! Is it plugged in?")
    # Check if running on Windows
    if platform.system() != "Windows":
        raise RuntimeError("This code only works on Windows. Detected OS: " + platform.system())
    return 3, 48000


def resample_audio(samples: np.ndarray, input_rate, output_rate, output_int16=True) -> np.ndarray:
    """
    samples: int16 mono input at input_rate
    returns: int16 mono output at output_rate
    """
    if input_rate == output_rate:
        return samples
    # Convert to float for resampling
    samples_f = samples.astype(np.float32)

    # Resample
    resampled = resample_poly(samples_f, output_rate, input_rate)

    if not output_int16:
        return resampled

    # Back to int16
    return np.clip(resampled, -32768, 32767).astype(np.int16)


def play_audio_file(file_path, out_device, play_samplerate, volume=0.3):
    sd.stop()
    data, samplerate = sf.read(file_path, dtype='float32')
    if samplerate != play_samplerate:
        data = resample_audio(data, samplerate, play_samplerate, output_int16=False)

    # Scale volume (keep float32)
    data = np.clip(data * volume, -1.0, 1.0)

    sd.play(data, play_samplerate, device=out_device)
    sd.wait()  # Wait until playback is done
