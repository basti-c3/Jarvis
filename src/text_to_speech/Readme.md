# Common errors during training, that you can fix yourself in the TTS source code
# ---------------1---------------
# AttributeError: 'TTS' object has no attribute 'is_multi_lingual' -> change in TTS/api.py property is_multi_lingual to:
# See https://github.com/coqui-ai/TTS/issues/3449
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

# ---------------2---------------
# Missing key(s) in state_dict: "disc.nets.0.convs.0.bias" --> introduce strict parameter that goes through the
# functions with value false until just before the place where the error happens (load_checkpoint, see traceback)