import os

from TTS.api import TTS
from src.text_to_speech.VoiceConversionModel import VoiceConversionModel
from src.text_to_speech.utils import DEFAULT_OUT_TEXT


def tts_from_saved_model(model_path, config_path, output_path=None, text=DEFAULT_OUT_TEXT, **kwargs):
    model_dir, model_filename = os.path.split(model_path)
    model = VoiceConversionModel(checkpoint_path=model_path, config_path=config_path)
    model.text_to_speech(model_dir_path=model_dir, text=text, model_filename=model_filename, output_path=output_path,
                         **kwargs)


def tts_from_vctk_vits(text=DEFAULT_OUT_TEXT, output_path=None, speaker="p225"):
    # Vits model storage place
    model_path = "C:/Users/basti/AppData/Local/tts/tts_models--en--vctk--vits/model_file.pth"
    config_path = "C:/Users/basti/AppData/Local/tts/tts_models--en--vctk--vits/config.json"

    tts_from_saved_model(model_path, config_path, output_path, text, speaker=speaker)


def speak_with_quick_voice_cloner(speaker_wav_path, text=DEFAULT_OUT_TEXT, output_path=None, language="en"):
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

    tts = TTS(model_name=model_name).to("cuda")
    # Generate speech
    tts.tts_to_file(text, speaker_wav=speaker_wav_path, file_path=output_path, language=language)
