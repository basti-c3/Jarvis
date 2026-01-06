import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import resample_poly


def play_audio_file(file_path, out_device, play_samplerate):
    data, samplerate = sf.read(file_path, dtype='float32')
    if samplerate != play_samplerate:
        data = resample_audio(data, samplerate, play_samplerate)
    sd.play(data, play_samplerate, device=out_device)
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


def print_output_device_info(name_substring="Anker"):
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_output_channels'] > 0 and name_substring.lower() in dev['name'].lower():
            print(f"Device {i}: {dev['name']}")
            print(f"Max output channels: {dev['max_output_channels']}")
            print(f"Default samplerate: {dev['default_samplerate']}")
            # Try opening a test stream
            try:
                with sd.OutputStream(device=i, samplerate=dev['default_samplerate'],
                                     channels=dev['max_output_channels']):
                    print("Stream OK at default samplerate")
            except Exception as e:
                print(f"Cannot open stream at default samplerate: {e}")
            break
    else:
        print("No Anker speaker found")


print_output_device_info()
