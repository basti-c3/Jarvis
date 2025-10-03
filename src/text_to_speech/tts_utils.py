import os
import torch

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs, Xtts
from TTS.config.shared_configs import BaseDatasetConfig

from TTS.api import TTS
from src.text_to_speech.VoiceConversionModel import VoiceConversionModel
from src.text_to_speech.utils import DEFAULT_OUT_TEXT, XTTS_MODEL_PATH


def tts_from_existing_model(model: str, base_path, text=DEFAULT_OUT_TEXT, output_path=None, speaker="p225"):
    model_name = {
        "lj": "tts_models--en--ljspeech--vits",
        "vctk": "tts_models--en--vctk--vits",
        "xtts": "tts_models--multilingual--multi-dataset--xtts_v2",
        "your_tts": "tts_models--multilingual--multi-dataset--your_tts",
    }
    if model not in model_name.keys():
        raise ValueError(f"Wrong model input {model}")
    kwargs = {}

    model_filename = 'model_file'
    if model == "xtts":
        model_filename = 'model'  # whyever
        kwargs['disable_adding_model_name'] = True
        kwargs['speaker'] = 'Damien Black'
        kwargs['language'] = 'en'
        # Allow some TTS classes, so that torch does not throw an error
        torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])
    elif model == "your_tts":
        kwargs['speaker'] = 'male-en-2'  # ['male-pt-3\n', 'female-en-5\n', 'female-en-5', 'male-en-2\n', 'male-en-2']
        kwargs['language'] = 'en'

    model_dir = os.path.join(base_path, model_name[model])
    model_path = os.path.join(model_dir, model_filename + '.pth')
    config_path = os.path.join(base_path, model_name[model], 'config.json')

    if not os.path.exists(model_path) or not os.path.exists(config_path):
        raise FileNotFoundError(f"model at {model_path} or config at {config_path} not found")

    if model == "vctk":
        kwargs['speaker'] = speaker

    model = VoiceConversionModel(checkpoint_path=model_path, config_path=config_path)
    model.text_to_speech(model_dir_path=model_dir, text=text, model_filename=model_filename, output_path=output_path,
                         **kwargs)


def load_xtts_model_from_checkpoint():
    model_name = XTTS_MODEL_PATH

    # First allow some TTS classes, so that torch does not throw an error
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

    return TTS(model_name=model_name).to("cuda")


def speak_with_quick_voice_cloner(speaker_wav_path=None, speaker_name=None, text=DEFAULT_OUT_TEXT, output_path=None,
                                  language="en"):
    if speaker_name is None and speaker_wav_path is None:
        raise ValueError("Either speaker_wav_path or speaker_name has to be given, both was None.")
    tts = load_xtts_model_from_checkpoint()

    # Generate speech
    try:
        tts.tts_to_file(text, speaker=speaker_name, speaker_wav=speaker_wav_path, file_path=output_path,
                        language=language)
    except KeyError as e:
        if speaker_name in str(e):
            raise KeyError(
                f"Speaker name {speaker_name} was not found in speakers_xtts. Have you added the speaker yourself before? If not, call create_new_speaker and exchange the speakers_xtts file by the new one")
        else:
            raise KeyError(e)


def create_new_speaker(new_speaker_name, wav_dir_path, delete_rest=False):
    # Path to your speakers_xtts.pth (adjust to your system)
    pth_path = r"C:\Users\basti\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\speakers_xtts.pth"
    new_pth_path = r"C:\Users\basti\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\speakers_xtts.pth"
    # Load dictionary
    speakers = torch.load(pth_path, map_location="cpu")

    [avg_gpt_cond_latent, avg_speaker_embedding, mdn_gpt_cond_latent,
     mdn_speaker_embedding] = create_new_speaker_embedding_for_xtts_model(wav_dir_path)

    speakers[new_speaker_name] = {'gpt_cond_latent': mdn_gpt_cond_latent, 'speaker_embedding': mdn_speaker_embedding}
    speakers[new_speaker_name + '_avg'] = {'gpt_cond_latent': avg_gpt_cond_latent,
                                           'speaker_embedding': avg_speaker_embedding}

    if delete_rest:
        speaker_names = [name for name in speakers.keys()]
        for name in speaker_names:
            if name not in [new_speaker_name, new_speaker_name + "_avg"]:
                del speakers[name]

    if len(speakers) == 1:
        # add dummy, as a multilingual model has to have at least two speakers
        speakers['dummy'] = {'gpt_cond_latent': None, 'speaker_embedding': None}
    print(f"Created new speaker {new_speaker_name} to be saved in file {new_pth_path}")
    torch.save(speakers, new_pth_path)


def create_new_speaker_embedding_for_xtts_model(wav_dir_path):
    tts: TTS = load_xtts_model_from_checkpoint()
    xtts: Xtts = tts.synthesizer.tts_model

    gpt_cond_latents = []
    speaker_embeddings = []
    i = 1

    for file in os.listdir(wav_dir_path):
        if file.endswith(".wav"):
            wav_path = os.path.join(wav_dir_path, file)
            gpt_cond_latent, speaker_embedding = xtts.get_conditioning_latents(
                audio_path=wav_path,
                gpt_cond_len=30,
                gpt_cond_chunk_len=4,
                max_ref_length=30,
                sound_norm_refs=False,
            )
            gpt_cond_latents.append(gpt_cond_latent)
            speaker_embeddings.append(speaker_embedding)
            print(f"{i}/{len(os.listdir(wav_dir_path))}")
            i += 1

    # Stack and average
    avg_gpt_cond_latent = torch.mean(torch.stack(gpt_cond_latents), dim=0)
    avg_speaker_embedding = torch.mean(torch.stack(speaker_embeddings), dim=0)

    mdn_gpt_cond_latent = torch.mean(torch.stack(gpt_cond_latents), dim=0)
    mdn_speaker_embedding = torch.mean(torch.stack(speaker_embeddings), dim=0)

    return avg_gpt_cond_latent, avg_speaker_embedding, mdn_gpt_cond_latent, mdn_speaker_embedding
