from datetime import datetime
import numpy as np
import json

from global_init import stt_model


def turn_speech_to_text(audio: np.array):
    # Ensure the vosk buffer is in the correct format (16kHz, mono, PCM 16-bit)
    start = datetime.now()
    if isinstance(audio, np.ndarray):
        if audio.dtype != np.int16:
            print(f"Converting audio to int16 format... from {audio.dtype}")
            audio = audio.astype(np.int16)
        audio_bytes = audio.tobytes()
    else:
        # If your buffer is in a different format (e.g., stereo), you may need to convert it
        # Ensure the buffer is the right type (16-bit PCM)
        raise Exception(f"Error in speech_to_text: Convert audio to right type before processing! Got {type(audio)}")

    if stt_model.recognizer.AcceptWaveform(audio_bytes):
        result = stt_model.recognizer.Result()
    else:
        result = stt_model.recognizer.FinalResult()

    # Parse the result
    result_dict = json.loads(result)
    recognized_text = result_dict.get('text', "")

    print("Result dict:", result_dict)
    end = datetime.now()
    print("Time to process the command", end - start)
    return recognized_text
