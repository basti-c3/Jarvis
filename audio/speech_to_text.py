# Load the Whisper models
import whisper

from audio.utils import Warn

base_model = whisper.load_model("base")
large_model = whisper.load_model("large")


def speech_to_text(audio, model_type="base"):
    if model_type not in ["base", "large"]:
        Warn(f"Error in speech_to_text: model_type {model_type} unknown. Fall back to model_type base")
        model_type = "base"

    if model_type == "base":
        model = base_model
    elif model_type == "large":
        model = large_model
    else:
        raise Exception("Error in speech_to_text: model not defined")

    return model.transcribe(audio, fp16=False)
