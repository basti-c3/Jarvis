import numpy as np

from audio import config
from audio.speech_to_text import speech_to_text


def record_command(audio_buffer: np.array, pause_audio_buffer: np.array, new_audio_chunk: np.array):
    # Append the new chunk to the pause detection buffer
    pause_audio_buffer = np.concatenate((pause_audio_buffer, new_audio_chunk))

    pause_buffer_long_enough = len(pause_audio_buffer) > config.RATE * config.COMMAND_END_PAUSE_LENGTH

    is_end = pause_buffer_long_enough and np.mean(np.abs(pause_audio_buffer)) < config.SILENCE_THRESHOLD
    command_length_exceeded = len(audio_buffer) > config.RATE * config.MAX_COMMAND_LENGTH

    if is_end or command_length_exceeded:
        if is_end:
            print("Detected pause in speech. Ending command capture...")
        else:
            print(f"Maximum command length of {config.MAX_COMMAND_LENGTH} was reached. Ending command capture...")
        process_command(audio_buffer)  # Process command
        return True, pause_audio_buffer
    if pause_buffer_long_enough:
        # Remove the first vosk chunk to maintain the same length
        pause_audio_buffer = pause_audio_buffer[len(new_audio_chunk):]
    return False, pause_audio_buffer


def process_command(audio):
    if config.DEV:
        result_command = speech_to_text(audio)
    else:
        result_command = speech_to_text(audio, "large")
    print("--------------------------------------------------------")
    print(f"Recognized Command: {result_command}")

    result_txt_lower = result_command.lower()
    keyword_index = result_txt_lower.find(config.KEYWORD)
    if keyword_index != -1:
        # Calculate the starting position of the text after the keyword
        start_index = keyword_index + len(config.KEYWORD)

        # Slice the string to get the text after the keyword
        text_after_keyword = result_command[start_index:].strip()

        print(f"Text following the keyword '{config.KEYWORD}': {text_after_keyword}")

        if 'turtle' in text_after_keyword.lower():
            print("Turtle recognized!!!")
    else:
        print(f"The keyword '{config.KEYWORD}' was not found in the text.")
