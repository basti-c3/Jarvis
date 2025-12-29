import json
from datetime import datetime

import numpy as np
import shared.stt_config as config
from shared.global_init import get_stt_recognizer


def get_command_text(audio_bytes):
    result_command = turn_speech_to_text(audio_bytes)
    print("--------------------------------------------------------")
    print(f"Recognized Command: {result_command}")

    result_txt_lower = result_command.lower()
    keyword_index = result_txt_lower.find(config.KEYWORD)
    if keyword_index != -1:
        # Calculate the starting position of the text after the keyword
        start_index = keyword_index + len(config.KEYWORD)

        # Slice the string to get the text after the keyword
        text_after_keyword = result_command[start_index:].strip()
        return text_after_keyword
    else:
        raise Exception(f"Error in get_command_text: The keyword '{config.KEYWORD}' was not found in the text.")


def turn_speech_to_text(audio_bytes):
    start = datetime.now()
    recognizer = get_stt_recognizer()
    if recognizer.AcceptWaveform(audio_bytes):
        result = recognizer.Result()
    else:
        result = recognizer.FinalResult()

    # Parse the result
    result_dict = json.loads(result)
    recognized_text = result_dict.get('text', "")

    print("Result dict:", result_dict)
    end = datetime.now()
    print("Time to process the command", end - start)
    return recognized_text
