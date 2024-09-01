from audio.global_vars import audio_queue


def audio_callback(indata, frames, time, status):
    """Callback function for sounddevice to receive vosk data."""
    if status:
        print(status, flush=True)
    # Convert vosk data to bytes and put it in the queue
    audio_queue.put(indata.copy())