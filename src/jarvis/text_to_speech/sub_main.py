from text_to_speech.DataClean import DataClean
from text_to_speech.VoiceConversionModel import VoiceConversionModel
from text_to_speech.tts_utils import create_new_speaker
from text_to_speech.tts_utils import speak_with_quick_voice_cloner, tts_from_existing_model

if __name__ == "__main__":
    desired_sample_rate = 22050
    speaker_name = "jarvis_avg"
    base_path = "C:/Users/basti/AppData/Local/tts/"
    speaker_wav_path = "../../data/voice_cloning/Jarvis/jarvis.wav"  #
    voice_dir_path = "../../data/voice_cloning/Basti/training/wavs"
    data_dir_path = "../../data/voice_cloning/Jarvis"
    model_dir_path = "../../data/voice_cloning/Jarvis/Jarvis_voice_model-June-17-2025_02+01AM-ea812f1"
    language = "en"
    output_text = "Play hard, work less. This is America."
    output_path = "../../data/voice_cloning/jarvis_avg_test_reihe2_test_audio_output.wav"

    # Options what to do
    clean_data_and_review_data = False
    train_model = False
    recalculate_phonemes = False
    create_audio_output = False
    create_vctk_vits_audio_output = False
    quick_xtts_audio_output = True
    create_new_speaker_id = False

    epoch_output_wav_interval = 1

    cleaner = DataClean(data_dir_path, required_sample_rate=desired_sample_rate)
    model = VoiceConversionModel(epoch_output_wav_interval=epoch_output_wav_interval)

    if clean_data_and_review_data:
        cleaner.run()

    if train_model:
        # If you changed something in the dataset: Set recalculate_phonemes=True
        model.set_test_directory(data_dir_path, recalculate_phonemes=recalculate_phonemes)
        model.fine_tune(epochs=100)

    if create_audio_output:
        model.text_to_speech(model_dir_path=model_dir_path)

    if create_vctk_vits_audio_output:
        tts_from_existing_model("lj", base_path, text=output_text, output_path=output_path)

    if quick_xtts_audio_output:
        speak_with_quick_voice_cloner(speaker_name=speaker_name, output_path=output_path, text=output_text,
                                      language=language)
        print(f"wav output saved to {output_path}")

    if create_new_speaker_id:
        create_new_speaker(speaker_name, voice_dir_path, False)  # or as wav_dir_path: [speaker_wav_path]
