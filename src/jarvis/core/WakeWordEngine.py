import os

import pvporcupine

from paths import WAKE_WORD_PATH


class WakeWordEngine:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
            keyword_paths=[WAKE_WORD_PATH],
            sensitivities=[0.6],
        )

    def process(self, pcm):
        return self.porcupine.process(pcm)

    def frame_length(self):
        return self.porcupine.frame_length

    def sample_rate(self):
        return self.porcupine.sample_rate
