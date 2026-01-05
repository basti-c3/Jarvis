import os.path
import platform

import torch
import winsound


def review_speakers():
    pth_path = r"C:\Users\basti\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\speakers_xtts.pth"
    speakers = torch.load(pth_path, map_location="cpu")
    for name, embedding in speakers.items():
        print(name)


# review_speakers()


def create_jarvis_output(sentences):
    from tts.text_to_speech_dev.tts_utils import speak_with_quick_voice_cloner
    speaker_name = "jarvis_avg"
    language = "en"

    for sentence in sentences:
        output_text = sentence
        sentence = sentence.replace(",", "")
        sentence = sentence.replace(".", "")
        sentence = sentence.replace("!", "")
        sentence = sentence.replace("?", "")
        sentence = sentence.replace(";", "")
        sentence = sentence.replace(" ", "")
        sentence = sentence.replace("'", "")

        output_path = f"../../data/precalculated_jarvis_audios/{sentence.lower()}.wav"
        print(os.path.abspath(output_path))
        speak_with_quick_voice_cloner(speaker_name=speaker_name, output_path=output_path, text=output_text,
                                      language=language)
        print(f"wav output saved to {output_path}")


sentences = [
    "Shutting down. Goodbye Sir.",
]
create_jarvis_output(sentences)

if platform.system() == "Windows":
    # Uses built-in Windows sound player

    filepath = f"../../data/precalculated_jarvis_audios/abcdefg.wav"
    winsound.PlaySound(filepath, winsound.SND_FILENAME)
