from global_init import audio_queue


def audio_callback(indata, frames, time, status):
    """Callback function for sounddevice to receive audio data."""
    if status:
        print(status, flush=True)
    # Convert vosk_model data to bytes and put it in the queue
    audio_queue.put(indata.copy())