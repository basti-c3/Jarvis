import os

from TTS.api import TTS
from TTS.config import load_config
from trainer import Trainer, TrainerArgs
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsAudioConfig
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor
from jarvis.paths import METADATA_FILENAME, CLEAN_DATA_DIR_NAME, VITS_MODEL_PATH, VITS_CONFIG_PATH, DEFAULT_OUT_TEXT


class VoiceConversionModel:
    def __init__(
            self,
            checkpoint_path=VITS_MODEL_PATH,
            config_path=VITS_CONFIG_PATH,
            eval_split_max_size=5,
            sample_rate_of_test_data=22050,
            batch_size=16,
            eval_batch_size=8,
            batch_group_size=1,
            num_loader_workers=8,
            learning_rate=5e-5,  # For fine-tuning lower learning rate required
            epoch_output_wav_interval=5,
    ):
        self.pretrained_checkpoint_path = checkpoint_path
        self.checkpoint_config_path = config_path

        self.eval_split_max_size = eval_split_max_size
        self.sample_rate = sample_rate_of_test_data
        self.epoch_output_wav_interval = epoch_output_wav_interval

        self.num_loader_workers = num_loader_workers
        self.batch_size = batch_size
        self.eval_batch_size = eval_batch_size
        self.batch_group_size = batch_group_size
        self.learning_rate = learning_rate

        # Set in set_test_directory
        self.clone_dir_path = None
        self.phoneme_cache_path = None
        self.actual_data_path = None
        self.metadata_path = None

        # Set during training
        self.model_dir_path = None

    def set_test_directory(self, clone_dir_path, recalculate_phonemes=False):
        if clone_dir_path is None:
            raise ValueError("test_data_path cannot be None at this point, but is.")
        if not os.path.exists(clone_dir_path):
            raise FileNotFoundError(f"test_data_path {os.path.abspath(clone_dir_path)} does not exist")

        actual_data_path = os.path.join(clone_dir_path, CLEAN_DATA_DIR_NAME)
        if not os.path.exists(actual_data_path):
            raise FileNotFoundError(f"cleaned test data {os.path.abspath(actual_data_path)} does not exist")

        metadata_path = os.path.join(actual_data_path, METADATA_FILENAME)
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"meta data at {os.path.abspath(metadata_path)} does not exist")

        wav_files_path = os.path.join(actual_data_path, 'wavs')
        if not os.path.exists(wav_files_path):
            raise FileNotFoundError(f"wavs directory {os.path.abspath(wav_files_path)} does not exist")

        wav_files_count = len([file for file in os.listdir(wav_files_path) if file.endswith('.wav')])
        if wav_files_count == 0:
            raise FileNotFoundError(f"wavs directory {os.path.abspath(wav_files_path)} does have any .wav files")

        phoneme_cache_path = os.path.join(clone_dir_path, "phoneme_cache")
        if recalculate_phonemes:
            if os.path.exists(phoneme_cache_path):
                os.remove(phoneme_cache_path)

        self.clone_dir_path = clone_dir_path
        self.phoneme_cache_path = phoneme_cache_path
        self.actual_data_path = actual_data_path
        self.metadata_path = metadata_path

    def after_epoch(self, trainer: Trainer):
        epoch_idx = trainer.epochs_done
        if epoch_idx % self.epoch_output_wav_interval == 0:
            print(f"Running TTS output at epoch {epoch_idx}")
            self.text_to_speech(out_filename=f"tts_output_{epoch_idx}.wav")

    def fine_tune(self, epochs=100):
        if self.clone_dir_path is None:
            raise ValueError("clone_dir_path is None. Have you called set_test_directory to set up everything?")

        # Load data samples
        dataset_config = BaseDatasetConfig(formatter="ljspeech", meta_file_train=METADATA_FILENAME,
                                           path=self.actual_data_path)
        train_samples, eval_samples = load_tts_samples(
            dataset_config,
            eval_split=True,
            eval_split_max_size=self.eval_split_max_size,
        )

        config = load_config(self.checkpoint_config_path)
        config.audio = VitsAudioConfig(
            sample_rate=self.sample_rate, win_length=1024, hop_length=256, num_mels=80, mel_fmin=150, mel_fmax=8000
        )
        config.output_path = self.clone_dir_path
        config.run_name = f"{os.path.basename(self.clone_dir_path)}_voice_model"
        config.batch_size = self.batch_size
        config.eval_batch_size = self.eval_batch_size
        config.batch_group_size = self.batch_group_size
        config.eval_split_max_size = self.eval_split_max_size
        config["lr_gen"] = self.learning_rate
        config["lr_disc"] = self.learning_rate
        config.num_loader_workers = self.num_loader_workers
        config.num_eval_loader_workers = int(self.num_loader_workers / 2)  # reduces memory, eval isn't as often
        config.run_eval = True
        config.test_delay_epochs = -1
        config.epochs = epochs  # Number of epochs, for fine tuning not as big as for training from scratch
        config.text_cleaner = "english_cleaners"
        config.use_phonemes = True  # Makes voice smoother (at least I think it does)
        config.phoneme_language = "en-gb"
        config.phoneme_cache_path = self.phoneme_cache_path
        config.compute_input_seq_cache = True
        config.print_step = 25
        config.print_eval = True
        config.mixed_precision = True
        config.datasets = [dataset_config]
        config.cudnn_benchmark = False
        config.model_args.init_discriminator = True  # Relevant for not getting error that self.disc does not exist

        ap = AudioProcessor.init_from_config(config)
        tokenizer, config = TTSTokenizer.init_from_config(config)

        model = Vits(config, ap, tokenizer)
        # Set strict=False to not require all checkpoint weights to exist, if some don't (e.g. disc) it's ok
        model.load_checkpoint(config, self.pretrained_checkpoint_path, strict=False)

        # Initialize the trainer for fine-tuning
        trainer = Trainer(
            TrainerArgs(),
            config,
            self.clone_dir_path,
            model=model,
            train_samples=train_samples,
            eval_samples=eval_samples,
            callbacks={
                'on_epoch_end': self.after_epoch  # To be able to produce outputs on runtime
            }
        )
        self.model_dir_path = trainer.output_path

        trainer.fit()

        # Final output text to speech
        self.text_to_speech(out_filename="final_output_audio")

    def text_to_speech(self, model_dir_path=None, text=DEFAULT_OUT_TEXT, model_filename="best_model", output_path=None,
                       out_filename='output_audio', **kwargs):
        # Provide either a full output_path or just out_filename to be saved in the same dir as the model is in
        self.model_dir_path = model_dir_path if model_dir_path is not None else self.model_dir_path
        if self.model_dir_path is None:
            raise ValueError("Please provide the model_dir_path")
        if kwargs.pop('disable_adding_model_name', None):
            model_path = self.model_dir_path
        else:
            model_path = os.path.join(self.model_dir_path, f"{model_filename}.pth")
        config_path = os.path.join(self.model_dir_path, f"config.json")

        if not os.path.exists(model_path) or not os.path.exists(config_path):
            raise FileNotFoundError(f"Either model or config path dont exist: {model_path}, {config_path}")

        tts = TTS(model_path=model_path, config_path=config_path, strict=False).to("cuda")
        out_file_path = os.path.join(self.model_dir_path, out_filename + '.wav') if output_path is None else output_path
        tts.tts_to_file(text, file_path=out_file_path, **kwargs)

        print(f"Successfully created output {out_filename}!")
