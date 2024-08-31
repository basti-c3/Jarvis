import os

from vosk import Model, KaldiRecognizer
import numpy as np

from audio import config
from audio.utils import Warn
import json


def speech_to_text(audio: np.array, model_type="en"):
    if model_type not in ["en", "de"]:
        Warn(f"Error in speech_to_text: model_type {model_type} unknown. Fall back to model_type base")
        model_type = "en"

    if model_type == "en":
        model_path = "models/vosk-model-small-en-us-0.15"
    elif model_type == "de":
        model_path = ""  # todo
    else:
        raise Exception("Error in speech_to_text: model not defined")

    if not os.path.exists(model_path):
        print("Please give the correct path to the model you are looking for.")
        exit(1)

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, config.RATE)

    # Ensure the audio buffer is in the correct format (16kHz, mono, PCM 16-bit)
    if isinstance(audio, np.ndarray):
        if audio.dtype != np.int16:
            print(f"Converting audio to int16 format... from {audio.dtype}")
            audio = audio.astype(np.int16)
        audio_bytes = audio.tobytes()
    else:
        # If your buffer is in a different format (e.g., stereo), you may need to convert it
        # Ensure the buffer is the right type (16-bit PCM)
        raise Exception(f"Error in speech_to_text: Convert audio to right type before processing! Got {type(audio)}")

    if recognizer.AcceptWaveform(audio_bytes):
        result = recognizer.Result()
    else:
        result = recognizer.FinalResult()

    # Parse the result
    result_dict = json.loads(result)
    recognized_text = result_dict.get('text', "")

    print("Result dict:", result_dict)
    return recognized_text
