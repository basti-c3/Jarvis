import traceback

import numpy as np

from audio import config
from audio.global_vars import audio_queue
from audio.process_command import process_command
from audio.speech_to_text import speech_to_text


def process_audio():
    """
        Continuously process audio data from the queue and perform speech recognition
        to detect if a command is coming in.
     """
    print("Listening for the word 'Jarvis'...")

    # Buffer to hold audio for each recognition pass
    audio_buffer = np.array([], dtype=np.int16)
    pause_audio_buffer = np.array([], dtype=np.int16)  # Checking for a longer pause in commands
    is_recording_command = False

    while True:
        try:
            reset_buffers = False

            # Get audio data from the queue
            audio_chunk = audio_queue.get()

            # Append the chunk to the buffer
            audio_buffer = np.concatenate((audio_buffer, audio_chunk))

            # When buffer is long enough, run simple text recognition, check for keyword and reset buffer
            run_process = len(audio_buffer) > config.RATE * config.AUDIO_CHUNK_LENGTH

            if is_recording_command:
                # This code is run multiple times until a long enough pause is detected --> command_finished = True
                command_finished, pause_audio_buffer = record_command(audio_buffer, pause_audio_buffer, audio_chunk)
                if command_finished:
                    is_recording_command = False
                    if config.DEV:
                        # In DEV, only one command needed, stop listening after processing the command
                        return
                    reset_buffers = True
            elif run_process:
                # This code is run once, every AUDIO_CHUNK_LENGTH seconds
                found_keyword = False
                speech_detected = np.mean(np.abs(audio_buffer)) > config.SILENCE_THRESHOLD
                if speech_detected:
                    found_keyword = check_for_keyword(audio_buffer) if speech_detected else False
                if found_keyword:
                    is_recording_command = True
                    # Do not reset buffers here, as the command starts in this buffer and is needed for processing
                else:
                    reset_buffers = True
            else:
                continue  # Nothing happened, next iteration

            if reset_buffers:
                # Reset the buffers
                last_half_second_audio = audio_buffer[-config.OVERLAP_SIZE:]
                audio_buffer = last_half_second_audio
                pause_audio_buffer = np.array([], dtype=np.float32)

        except Exception as e:
            print(f"Error recognizing audio: {e}")
            traceback.print_exc()


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
        # Remove the first audio chunk to maintain the same length
        pause_audio_buffer = pause_audio_buffer[len(new_audio_chunk):]
    return False, pause_audio_buffer


def check_for_keyword(audio_buffer: np.array):
    print("Processing audio chunk...")

    # Run recognition on the accumulated audio with simpler model
    result_txt = speech_to_text(audio_buffer)

    # Print recognized text
    print(f"Got: {result_txt}")

    # Check for the keyword "Jarvis"
    if config.KEYWORD in result_txt.lower():
        print("Keyword 'Jarvis' detected! Start recording command...")
        return True
    return False
