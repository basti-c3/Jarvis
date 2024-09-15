import os

from trainer import Trainer, TrainerArgs

from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsArgs, VitsAudioConfig
from TTS.tts.utils.speakers import SpeakerManager
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor


def train():
    # If you want to do transfer learning and speedup your training you can set here the path to the original YourTTS model
    RESTORE_PATH = "C:/Users/basti/AppData/Local/tts/tts_models--en--vctk--vits/model_file.pth"

    TRAINING_EPOCHS = 50  # Set number of training epochs
    EVAL_SPLIT_SIZE = 8  # usually config.eval_split_size = 1% of the given samples as evaluation (only for over 100 speech samples)

    BATCH_SIZE = 8

    LEARNING_RATE = 0.0001  # Usually 0.0002

    SAMPLE_RATE = 16000  # 22050

    RUN_NAME = "Basti_audio_vits_test"

    # Path where you want to save the models outputs (configs, checkpoints and tensorboard logs)
    OUT_PATH = f"./{RUN_NAME}"
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    # This paramter is useful to debug, it skips the training epochs and just do the evaluation and produce the test sentences
    SKIP_TRAIN_EPOCH = False

    dataset_config = BaseDatasetConfig(
        formatter="vctk",  # Adjust if your dataset format differs
        dataset_name="basti_audio",
        meta_file_train="",
        meta_file_val="",
        path="Basti_audio",
        language="en",  # Set language accordingly
    )

    audio_config = VitsAudioConfig(
        sample_rate=SAMPLE_RATE, win_length=1024, hop_length=256, num_mels=80, mel_fmin=0, mel_fmax=8000
    )

    vitsArgs = VitsArgs(
        use_speaker_embedding=True,
    )

    config = VitsConfig(
        model_args=vitsArgs,
        audio=audio_config,
        run_name=RUN_NAME,
        batch_size=BATCH_SIZE,
        lr_disc=LEARNING_RATE,
        lr_gen=LEARNING_RATE,
        eval_batch_size=int(BATCH_SIZE / 2),
        batch_group_size=5,
        num_loader_workers=4,
        num_eval_loader_workers=4,
        run_eval=True,
        test_delay_epochs=-1,
        epochs=TRAINING_EPOCHS,  # Set number of training epochs
        text_cleaner="english_cleaners",
        use_phonemes=True,
        phoneme_language="en",
        phoneme_cache_path=os.path.join(OUT_PATH, "phoneme_cache"),
        compute_input_seq_cache=True,
        print_step=50,
        plot_step=100,
        log_model_step=1000,
        save_step=5000,
        save_n_checkpoints=2,
        save_checkpoints=True,
        print_eval=False,
        mixed_precision=True,
        max_text_len=325,  # change this if you have a larger VRAM than 16GB
        output_path=OUT_PATH,
        datasets=[dataset_config],
        cudnn_benchmark=False,
        eval_split_size=EVAL_SPLIT_SIZE,
        dashboard_logger="tensorboard",
        logger_uri="./runs",
        test_sentences=[
            [
                "It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent.",
                "VCTK_basti",
                None,
                "en",
            ],
            [
                "Interesting development, I shall investigate further upon it.",
                "VCTK_basti",
                None,
                "en",
            ],
        ],
    )

    # INITIALIZE THE AUDIO PROCESSOR
    # Audio processor is used for feature extraction and audio I/O.
    # It mainly serves to the dataloader and the training loggers.
    ap = AudioProcessor.init_from_config(config)

    # INITIALIZE THE TOKENIZER
    # Tokenizer is used to convert text to sequences of token IDs.
    # config is updated with the default characters if not defined in the config.
    tokenizer, config = TTSTokenizer.init_from_config(config)

    # LOAD DATA SAMPLES
    # Each sample is a list of ```[text, audio_file_path, speaker_name]```
    # You can define your custom sample loader returning the list of samples.
    # Or define your custom formatter and pass it to the `load_tts_samples`.
    # Check `TTS.tts.datasets.load_tts_samples` for more details.
    train_samples, eval_samples = load_tts_samples(
        dataset_config,
        eval_split=True,
        eval_split_max_size=config.eval_split_max_size,
        eval_split_size=config.eval_split_size,
    )

    # init speaker manager for multi-speaker training
    # it maps speaker-id to speaker-name in the model and data-loader
    speaker_manager = SpeakerManager()
    speaker_manager.set_ids_from_data(train_samples + eval_samples, parse_key="speaker_name")
    config.model_args.num_speakers = speaker_manager.num_speakers

    # init model
    model = Vits(config, ap, tokenizer, speaker_manager).to("cuda")

    # init the trainer and 🚀
    trainer = Trainer(
        TrainerArgs(restore_path=RESTORE_PATH, skip_train_epoch=SKIP_TRAIN_EPOCH),
        config,
        OUT_PATH,
        model=model,
        train_samples=train_samples,
        eval_samples=eval_samples,
    )
    trainer.fit()


if __name__ == '__main__':
    train()
    # to see and hear progress, go into terminal into this directory and run
    # tensorboard --logdir=./runs
