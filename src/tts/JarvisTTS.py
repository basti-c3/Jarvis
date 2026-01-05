import numpy as np
import sounddevice as sd

from jarvis.paths import XTTS_MODEL_PATH
from tts.utils import load_xtts_model_from_checkpoint


class JarvisTTS:
    def __init__(self):
        self.model_path = XTTS_MODEL_PATH
        self.speaker_name = "jarvis_avg"
        self.language = "en"
        self.split_sentences = True

        self.tts = load_xtts_model_from_checkpoint()
        self.sample_rate = 24000

    def _convert_text_to_speech(self, text) -> list[float]:
        """Converts text to a list of integers (raw audio samples). Uses the speaker of the defined model."""
        #self.tts.tts_to_file(text, speaker=self.speaker_name, speaker_wav=None, file_path="./output_path", language=self.language)
        return self.tts.tts(text=text,
                            speaker=self.speaker_name,
                            speaker_wav=None,
                            # Either give speaker with precomputed voice embedding or speaker_wav file
                            language=self.language,
                            split_sentences=self.split_sentences)



    def create_and_play_audio_from_text(self, text):
        """Convert text to speech and play it through speakers."""
        audio_list = self._convert_text_to_speech(text)
        audio_array = np.array(audio_list, dtype=np.float32)
        print(f"Playing audio of length {len(audio_array)} samples at {self.sample_rate} Hz...")
        sd.play(audio_array, samplerate=self.sample_rate)
        sd.wait()