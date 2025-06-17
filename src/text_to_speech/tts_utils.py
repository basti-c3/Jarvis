import os
import torch

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

from TTS.api import TTS
from src.text_to_speech.VoiceConversionModel import VoiceConversionModel
from src.text_to_speech.utils import DEFAULT_OUT_TEXT


def tts_from_existing_model(model: str, base_path, text=DEFAULT_OUT_TEXT, output_path=None, speaker="p225"):
    model_name = {
        "lj": "tts_models--en--ljspeech--vits",
        "vctk": "tts_models--en--vctk--vits",
        "xtts": "tts_models--multilingual--multi-dataset--xtts_v2",
        "your_tts": "tts_models--multilingual--multi-dataset--your_tts",
    }
    if model not in model_name.keys():
        raise ValueError(f"Wrong model input {model}")
    kwargs = {}

    model_filename = 'model_file'
    if model == "xtts":
        model_filename = 'model'  # whyever
        kwargs['disable_adding_model_name'] = True
        kwargs['speaker'] = 'Damien Black'
        kwargs['language'] = 'en'
        # Allow some TTS classes, so that torch does not throw an error
        torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])
    elif model == "your_tts":
        kwargs['speaker'] = 'male-en-2'  # ['male-pt-3\n', 'female-en-5\n', 'female-en-5', 'male-en-2\n', 'male-en-2']
        kwargs['language'] = 'en'

    model_dir = os.path.join(base_path, model_name[model])
    model_path = os.path.join(model_dir, model_filename + '.pth')
    config_path = os.path.join(base_path, model_name[model], 'config.json')

    if not os.path.exists(model_path) or not os.path.exists(config_path):
        raise FileNotFoundError(f"model at {model_path} or config at {config_path} not found")

    if model == "vctk":
        kwargs['speaker'] = speaker

    model = VoiceConversionModel(checkpoint_path=model_path, config_path=config_path)
    model.text_to_speech(model_dir_path=model_dir, text=text, model_filename=model_filename, output_path=output_path,
                         **kwargs)


def speak_with_quick_voice_cloner(speaker_wav_path, text=DEFAULT_OUT_TEXT, output_path=None, language="en"):
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    # model_name = "tts_models--multilingual--multi-dataset--your_tts"

    # First allow some TTS classes, so that torch does not throw an error
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

    tts = TTS(model_name=model_name).to("cuda")
    # Generate speech
    tts.tts_to_file(text, speaker_wav=speaker_wav_path, file_path=output_path, language=language)
