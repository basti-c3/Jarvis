import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import resample_poly


def play_audio_file(file_path, out_device, play_samplerate, volume=0.3):
    data, samplerate = sf.read(file_path, dtype='float32')
    if samplerate != play_samplerate:
        data = resample_audio(data, samplerate, play_samplerate, output_int16=False)

    # Scale volume (keep float32)
    data = np.clip(data * volume, -1.0, 1.0)

    sd.play(data, play_samplerate, device=out_device)
    sd.wait()  # Wait until playback is done


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
