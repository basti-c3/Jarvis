import queue
import traceback

import numpy as np

import src.vosk_model.config as config
from src.global_init import audio_queue
from src.vosk_model.process_command import record_command
from src.vosk_model.speech_to_text import recognizer


def continuous_processing():
    """
        Continuously process audio data from the queue and perform speech recognition
        to detect if a command is coming in.
     """
    is_recording_command = False
    command_audio_buffer = np.array([], dtype=np.int16)
    command_pause_buffer = np.array([], dtype=np.int16)

    while True:
        try:
            # Get audio data from the queue
            audio_chunk = audio_queue.get(timeout=1)  # Get audio data from the queue
            if not is_recording_command:
                is_recording_command = keyword_detected(audio_chunk.tobytes())
            else:
                command_finished, command_audio_buffer, command_pause_buffer = record_command(command_audio_buffer,
                                                                                              command_pause_buffer,
                                                                                              audio_chunk.flatten())
                if command_finished:
                    # Reset buffers and command
                    is_recording_command = False
                    command_audio_buffer = np.array([], dtype=np.int16)
                    command_pause_buffer = np.array([], dtype=np.int16)
        except queue.Empty:
            continue  # Continue if the queue is empty
        except Exception as e:
            print(f"Error recognizing vosk_model: {e}")
            traceback.print_exc()


def keyword_detected(audio_bytes):
    if recognizer.AcceptWaveform(audio_bytes):
        result = recognizer.Result()
        print(f"Result: {result}")
        if config.KEYWORD in result.lower():
            return True

    else:
        partial_result = recognizer.PartialResult()
        print(f"Partial Result: {partial_result}")
        if config.KEYWORD in partial_result.lower():
            return True
