import threading

from global_init import get_tts_model
from utils import Warn



class Jarvis:
    processing = False

    def say(self, text):
        if self.processing:
            # Don't say multiple stuff at once
            return
        print("Dont wait for me,I am doing something parallelly. Processing...")
        def run():
            try:
                self.processing = True
                tts_model = get_tts_model()
                tts_model.create_and_play_audio_from_text(text)
            except Exception as e:
                Warn("Jarvis speaking error:", e)
            finally:
                self.processing = False

        threading.Thread(target=run, daemon=True).start()


jarvis = Jarvis()
