import numpy as np

from shared.Anker import anker
from jarvis.Jarvis import jarvis
from shared.utils import resample_audio
from shared import stt_config as config


def audio_callback(indata, frames, time, status):
    """Callback function for receiving audio data."""
    # Flatten and convert to int16
    pcm = indata[:, 0].astype(np.int16)
    pcm_resampled = resample_audio(pcm, anker.audio_mic_sample_rate, config.AUDIO_RATE)

    # Split into Porcupine-sized frames
    frame_len = jarvis.wake_word.frame_length()
    for i in range(0, len(pcm_resampled), frame_len):
        frame = pcm_resampled[i:i + frame_len]
        if len(frame) == frame_len:
            jarvis.audio_queue.put(frame)

    # Handle last partial frame (if any)
    remainder = len(pcm_resampled) % frame_len
    if remainder != 0:
        # Take the last frame_len samples ending at pcm[-1]
        last_frame = pcm_resampled[-frame_len:]

        # If pcm is shorter than frame_len, pad at the front
        if len(last_frame) < frame_len:
            pad_size = frame_len - len(last_frame)
            last_frame = np.pad(
                last_frame,
                (pad_size, 0),
                mode="constant"
            )

        jarvis.audio_queue.put(last_frame)
