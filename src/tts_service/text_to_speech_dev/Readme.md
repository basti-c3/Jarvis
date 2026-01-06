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
# ---------------3---------------
# Missing key(s) in state_dict: "disc.nets.0.convs.0.bias", ...
# This is, because some discriminator weights are expected. Introduce keyword parameter strict=True (default) until
# load_state_dict() uses this value and give it from your code as strict=False to the first TTS entry point, e.g. TTS()

# How to setup everything? 
You need nvidia graphic card with cu118 support for this setup. How to check this? Run in terminal:
nvidia-smi
search for this line --> Driver Version: x.x.x    CUDA Version: 11.8 <-- or newer!
If everything checks out run the following commands:

cd <path to jarvis>
conda create --name jarvis_env python=3.10
conda activate jarvis_env
pip install torch==2.7.1+cu118 torchvision==0.22.1+cu118 torchaudio==2.7.1 --index-url https://download.pytorch.org/whl/cu118
# Also get the whole TTS from git
git clone https://github.com/coqui-ai/TTS.git
cd TTS
pip install -r requirements.txt
pip install -e .
cd ..
pip install -r requirements.txt
# put <path to jarvis>\TTS into Umgebungsvariable PYTHONPATH
# Look to the start of this file for common error ---1--- and apply it to the corresponding TTS file

# Now you need the test data for training a model. Therfore you need in Jarvis/data/voice_cloning a folder including
# 1. cleaned_test_data/metadata.csv
# 2. cleaned_test_data/wavs/ including all .wav audio files (filenames only relevant for metadata.csv)