from src.text_to_speech.DataClean import DataClean
from src.text_to_speech.VoiceConversionModel import VoiceConversionModel
from src.text_to_speech.tts_utils import tts_from_saved_model, speak_with_quick_voice_cloner, \
    tts_from_vctk_vits

if __name__ == "__main__":
    desired_sample_rate = 22050
    speaker_wav_path = "../../data/voice_cloning/Jarvis/jarvis.wav"
    data_dir_path = "../../../data/voice_cloning/Jarvis"
    model_dir_path = "../../../data/voice_cloning/Jarvis/jarvis_voice_model-June-16-2025_03+17PM-1e4d37b"
    output_text = "Now listen. This is a test, and I do not want you to freak out."

    # Options what to do
    clean_data = False
    review_data = False
    train_model = False
    create_audio_output = False
    create_vctk_vits_audio_output = False
    quick_xtts_audio_output = False

    cleaner = DataClean(data_dir_path, required_sample_rate=desired_sample_rate)
    model = VoiceConversionModel()

    if clean_data:
        cleaner.run()
    if review_data:
        cleaner.review_audio_files()

    if train_model:
        # If you changed something in the dataset: Set recalculate_phonemes=True
        model.set_test_directory(data_dir_path, recalculate_phonemes=False)
        model.fine_tune(epochs=100)

    if create_audio_output:
        model.text_to_speech(model_dir_path=model_dir_path)

    if create_vctk_vits_audio_output:
        tts_from_vctk_vits(text=output_text)

    if quick_xtts_audio_output:
        speak_with_quick_voice_cloner(speaker_wav_path, text=output_text)
