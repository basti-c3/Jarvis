import os
from vosk import Model, KaldiRecognizer
import shared.stt_config as config
from jarvis.paths import STT_MODEL_PATH


class JarvisSTT:
    def __init__(self):
        self.model_path = STT_MODEL_PATH
        self.recognizer = None
        self.stt = None
        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            raise Exception(f"Error: No model at path {os.path.abspath(STT_MODEL_PATH)}")

        model = Model(STT_MODEL_PATH)
        recognizer = KaldiRecognizer(model, config.AUDIO_RATE)
        self.stt = model
        self.recognizer = recognizer
