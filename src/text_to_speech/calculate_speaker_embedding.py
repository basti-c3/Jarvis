
from TTS.api import TTS

model_name = "tts_models/multilingual/multi-dataset/your_tts"

model_path = "C:/Users/basti/AppData/Local/tts/tts_models--multilingual--multi-dataset--your_tts/model_file.pth"
config_path = "C:/Users/basti/AppData/Local/tts/tts_models--multilingual--multi-dataset--your_tts/config.json"

tts = TTS(model_name=model_name)

waveform, sample_rate = tts.load_audio("path_to_your_audio_file.wav")

embedding = tts.get_speaker_embedding(waveform)


# Print or save the embedding
print(embedding.shape)  # Should be (1, 512) for a single audio file
