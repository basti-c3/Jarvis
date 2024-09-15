import os

from TTS.config import load_config
from trainer import Trainer, TrainerArgs
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsAudioConfig
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

output_path = os.path.dirname(os.path.abspath("C:/Users/basti/Documents/Jarvis/data/voice_conversion/Basti"))
dataset_config = BaseDatasetConfig(
    formatter="ljspeech", meta_file_train="metadata.csv", path=os.path.join(output_path, "Basti/training/")
)
audio_config = VitsAudioConfig(
    sample_rate=22050, win_length=1024, hop_length=256, num_mels=80, mel_fmin=150, mel_fmax=9000
)

config = VitsConfig(
    audio=audio_config,
    run_name="jarvis_basti_voice_model",
    batch_size=16,
    eval_batch_size=8,
    batch_group_size=5,
    num_loader_workers=8,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=100,  # Reduced epochs for fine-tuning
    text_cleaner="english_cleaners",
    use_phonemes=True,
    phoneme_language="en-gb",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    compute_input_seq_cache=True,
    print_step=25,
    print_eval=True,
    mixed_precision=True,
    output_path=output_path,
    datasets=[dataset_config],
    cudnn_benchmark=False,
    eval_split_size=2, # How many of the given ones should be evaluation sets
)
config.model_args.init_discriminator = True # Otherwise error

# Lower learning rate for fine-tuning
config["lr_gen"] = 5e-5
config["lr_disc"] = 5e-5

# Initialize the audio processor
ap = AudioProcessor.init_from_config(config)

# Initialize the tokenizer
tokenizer, config = TTSTokenizer.init_from_config(config)

# Load data samples
train_samples, eval_samples = load_tts_samples(
    [dataset_config],
    eval_split=True,
    eval_split_max_size=config.eval_split_max_size,
    eval_split_size=config.eval_split_size,
)

# Load the pre-trained model and weights for fine-tuning
pretrained_checkpoint = "C:/Users/basti/AppData/Local/tts/tts_models--en--vctk--vits/model_file.pth"
checkpoint_config_path = "C:/Users/basti/AppData/Local/tts/tts_models--en--vctk--vits/config.json"
checkpoint_config = load_config(checkpoint_config_path)
checkpoint_ap = AudioProcessor.init_from_config(checkpoint_config)
checkpoint_tokenizer, checkpoint_config = TTSTokenizer.init_from_config(checkpoint_config)
model = Vits(checkpoint_config, checkpoint_ap, checkpoint_tokenizer, speaker_manager=None)
model.load_checkpoint(checkpoint_config, pretrained_checkpoint)

# Initialize the trainer for fine-tuning
trainer = Trainer(
    TrainerArgs(),
    config,
    output_path,
    model=model,
    train_samples=train_samples,
    eval_samples=eval_samples,
)

# Start fine-tuning
trainer.fit()

raise Exception("stop")

model_name = "tts_models/multilingual/multi-dataset/your_tts"

model_path = "C:/Users/basti/AppData/Local/tts/tts_models--multilingual--multi-dataset--your_tts/model_file.pth"
config_path = "C:/Users/basti/AppData/Local/tts/tts_models--multilingual--multi-dataset--your_tts/config.json"

tts = TTS(model_name=model_name)

# Load VITS config from pretrained model
# Config
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

dataset_path = "../../data/voice_conversion/Basti/training/wavs"
output_path_checkpoints = "checkpoints/"

if not os.path.exists(dataset_path):
    raise Exception(f"Path error: path {dataset_path} not found")

if not os.path.exists(output_path_checkpoints):
    os.makedirs(output_path_checkpoints)

trainer = VitsTrainer(config_path="vits_config_updated.yaml", model_name=model_name)
trainer.fit()

# --config_path "C:/Users/basti/Documents/Jarvis/src/text_to_speach/vits_training_config.json"

# First trial runs to get number of loaders. (between 1 and 4, wherever step time is lowest)
# eval_split_max_size smalller for gpu memory smaller (or batch size)

# tensorboard tensorboard --logdir=./runs (in the correct directory)
