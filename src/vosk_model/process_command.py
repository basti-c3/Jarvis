import numpy as np

import src.vosk_model.config as config
from src.global_init import spotify
from src.utils import Warn
from src.vosk_model.speech_to_text import speech_to_text


def record_command(audio_buffer: np.array, pause_buffer: np.array, new_audio_chunk: np.array):
    print("Audio buffer shape:", audio_buffer.shape)
    print("New audio chunk shape:", new_audio_chunk.shape)

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
        command_str = get_command_text(audio_buffer)
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
    if 'play' in command_str_lower and 'spotify' in command_str_lower:
        play_index = command_str_lower.find('play')
        spotify_index = command_str_lower.find('spotify')
        if play_index < spotify_index:  # play is before spotify in the query
            # Extract the substring between 'play' and 'spotify'
            extracted_command = command_str_lower[play_index + len('play'):spotify_index].strip()

            # Split to remove the word immediately before 'spotify'
            words = extracted_command.split()
            if len(words) > 1:
                # Remove the last word (the one immediately before 'spotify', for example 'on'/'in'/'with'/'from')
                words.pop()
                extracted_command = ' '.join(words)  # Join the remaining words to get the final result
        else:
            extracted_command = command_str_lower[play_index + len('play'):].strip()

        if 'artist' in extracted_command:  # remove artist from query and search for artists
            extracted_command = extracted_command.replace("artist", "")
            spotify.play_artist(extracted_command)
        elif 'song' in extracted_command:
            extracted_command = extracted_command.replace("song", "")
            spotify.play_track(extracted_command)
        elif 'album' in extracted_command:
            extracted_command = extracted_command.replace("album", "")
            spotify.play_album(extracted_command)
        else:
            # Default search for tracks
            spotify.play_track(extracted_command)
        print(f"Tried to handle extracted_command: {extracted_command}")
