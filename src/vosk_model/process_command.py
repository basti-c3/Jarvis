import numpy as np

import src.vosk_model.config as config

from src.spotify.SpotifyCommand import SpotifyCommand
from src.vosk_model.speech_to_text import speech_to_text


def record_command(audio_buffer: np.array, pause_buffer: np.array, new_audio_chunk: np.array, test_command=None):
    print("Recording command...")
    audio_buffer = np.concatenate((audio_buffer, new_audio_chunk))
    pause_buffer = np.concatenate((pause_buffer, new_audio_chunk))

    pause_buffer_long_enough = len(
        pause_buffer) > config.AUDIO_RATE * config.COMMAND_END_PAUSE_LENGTH
    is_end_of_command = pause_buffer_long_enough and np.mean(
        np.abs(pause_buffer)) < config.SILENCE_THRESHOLD

    if pause_buffer_long_enough:
        # Remove the first audio chunk to maintain the same length of the pause_buffer_long_enough
        pause_buffer = pause_buffer[len(new_audio_chunk):]

    command_length_exceeded = len(audio_buffer) > config.AUDIO_RATE * config.MAX_COMMAND_LENGTH
    if is_end_of_command or command_length_exceeded:
        if is_end_of_command:
            print("Detected pause in speech. Ending command capture...")
        else:
            print(f"Maximum command length of {config.MAX_COMMAND_LENGTH} was reached. Ending command capture...")
        command_str = get_command_text(audio_buffer) if test_command is None else test_command
        process_command(command_str)  # Process command
        return True, audio_buffer, pause_buffer
    return False, audio_buffer, pause_buffer


def get_command_text(audio):
    result_command = speech_to_text(audio)
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


def process_command(command_str):
    command_str_lower = command_str.lower()
    if 'play' in command_str_lower:
        spotify_command = SpotifyCommand(command_str)
        spotify_command.execute()

