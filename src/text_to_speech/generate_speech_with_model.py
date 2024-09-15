import os

from TTS.api import TTS


def speak_with_female_full_model(text="Example text", output_path="speech_output_samples/original_output.wav"):
    # Vits model storage place
    model_orig_path = "C:/Users/basti/AppData/Local/tts/tts_models--en--vctk--vits/model_file.pth"
    config_orig_path = "C:/Users/basti/AppData/Local/tts/tts_models--en--vctk--vits/config.json"

    # Initialize TTS
    tts = TTS(model_path=model_orig_path, config_path=config_orig_path, strict=False).to("cuda")
    tts.tts_to_file(text, speaker="p225", file_path=output_path)
    print("Successfully!")


def speak_with_trained_model(text, directory, model_filename="best_model", output_path="speech_output_samples/output.wav"):
    model_path = os.path.join(directory, f"{model_filename}.pth")
    config_path = os.path.join(directory, f"config.json")

    # Initialize TTS
    tts = TTS(model_path=model_path, config_path=config_path).to("cuda")
    tts.tts_to_file(text, file_path=output_path)
    print("Successfully!")


def speak_with_quick_voice_cloner(text, speaker_wav_path, output_path="speech_output_samples/output.wav", language="en"):
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

    tts = TTS(model_name=model_name).to("cuda")
    # Generate speech
    tts.tts_to_file(text, speaker_wav=speaker_wav_path, file_path=output_path, language=language)


if __name__ == "__main__":
    speaker_wav_path = "../../data/voice_conversion/Jarvis/jarvis.wav"

    text = "In the event of a sudden expression of joy, please be reminded, that this is not a final version of the voice, and will be further improved along the way."

    directory = "C:/Users/basti/Documents/Jarvis/src/text_to_speech/Basti_audio_vits_test/Basti_audio_vits_test-September-15-2024_03+54PM-c105a63/"

    speak_with_trained_model(text, directory, model_filename="best_model")
    # speak_with_female_full_model(text)
    # speak_with_quick_voice_cloner(text, speaker_wav_path)

################ Common errors that you can fix yourself in the TTS source code

# AttributeError: 'TTS' object has no attribute 'is_multi_lingual' --> change in TTS/api.py property is_multi_lingual to:
""" See https://github.com/coqui-ai/TTS/issues/3449
@property
def is_multi_lingual(self):
    if hasattr(self.synthesizer.tts_model, "language_manager") and self.synthesizer.tts_model.language_manager:
        return self.synthesizer.tts_model.language_manager.num_languages > 1
    if (
            isinstance(self.model_name, str)
            and "xtts" in self.model_name
            or self.config
            and "xtts" in self.config.model
    ):
        return True
    return False
"""

# Missing key(s) in state_dict: "disc.nets.0.convs.0.bias" --> introduce strict parameter that goes through the
# functions with value false until just before the place where the error happens (load_checkpoint, see traceback)
