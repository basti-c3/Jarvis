import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import resample_poly


def play_audio_file(file_path, play_samplerate=16000):
    data, samplerate = sf.read(file_path, dtype='float32')
    if samplerate != play_samplerate:
        data = resample_audio(data, samplerate, play_samplerate)
    sd.play(data, play_samplerate)
    sd.wait()  # Wait until playback is done


def resample_audio(samples: np.ndarray, input_rate, output_rate) -> np.ndarray:
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

    # Back to int16
    return np.clip(resampled, -32768, 32767).astype(np.int16)
