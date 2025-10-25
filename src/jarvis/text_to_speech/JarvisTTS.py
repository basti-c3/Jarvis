from text_to_speech.tts_utils import load_xtts_model_from_checkpoint
from paths import XTTS_MODEL_PATH


class JarvisTTS:
    def __init__(self):
        self.model_path = XTTS_MODEL_PATH
        self.speaker_name = "jarvis_avg"
        self.language = "en"
        self.split_sentences = True

        self.tts = load_xtts_model_from_checkpoint()

    def convert_text_to_speech(self, text):
        return self.tts.tts(text=text,
                            speaker=self.speaker_name,
                            speaker_wav=None,
                            # Either give speaker with precomputed voice embedding or speaker_wav file
                            language=self.language,
                            split_sentences=self.split_sentences)
