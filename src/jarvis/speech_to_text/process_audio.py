import queue
import traceback

import numpy as np
from collections import deque

import shared.stt_config as config
from Jarvis import jarvis
from shared.global_init import get_audio_queue, get_stt_recognizer
from shared.stop_event import stop_event
from speech_to_text.process_command import record_command
from shared.utils import Warn


def continuous_processing(test_command=None):
    """
        Continuously process audio data from the queue and perform speech recognition
        to detect if a command is coming in.
     """
    recognizer = get_stt_recognizer()

    is_recording_command = False
    detected_silence_time = 0
    command_audio_buffer = np.array([], dtype=np.int16)
    command_pause_buffer = np.array([], dtype=np.int16)
    pre_roll_buffer = deque(maxlen=config.PRE_ROLL_SAMPLES)

    if test_command:
        is_recording_command = True

    while not stop_event.is_set():
        try:
            # Get audio data from the queue
            audio_queue = get_audio_queue()
            audio_chunk = audio_queue.get(timeout=1)  # Get audio data from the queu
            pre_roll_buffer.extend(audio_chunk)

            if np.mean(np.abs(audio_chunk)) < config.SILENCE_THRESHOLD:
                detected_silence_time += config.BUFFER_DURATION
            else:
                detected_silence_time = 0

            if not is_recording_command:
                is_recording_command = keyword_detected(audio_chunk.tobytes())
                if is_recording_command:
                    command_audio_buffer = np.fromiter(pre_roll_buffer, dtype=np.int16) # Start the command with the keyword audio_chunk + some prebuffer
                    command_pause_buffer = command_audio_buffer.copy()
                elif not is_recording_command and detected_silence_time >= config.RESET_AUDIO_BUFFER_AFTER:
                    recognizer.Reset()
                    detected_silence_time = 0
                    pre_roll_buffer.clear()
                    command_audio_buffer = np.array([], dtype=np.int16)
                    command_pause_buffer = np.array([], dtype=np.int16)
            else:
                try:
                    command_finished, command_audio_buffer, command_pause_buffer = record_command(command_audio_buffer,
                                                                                                  command_pause_buffer,
                                                                                                  audio_chunk.flatten(),
                                                                                                  test_command)
                except Exception as error:
                    command_finished = True  # Reset buffers after error to start anew
                    Warn(str(error))
                    jarvis.say("Sorry Sir, but something went terribly wrong here, please try again.")
                finally:
                    if command_finished:
                        # Reset buffers and command
                        is_recording_command = False
                        recognizer.Reset()
                        pre_roll_buffer.clear()
                        command_audio_buffer = np.array([], dtype=np.int16)
                        command_pause_buffer = np.array([], dtype=np.int16)
        except queue.Empty:
            continue  # Continue if the queue is empty
        except Exception as e:
            print(f"Error recognizing vosk_model: {e}")
            traceback.print_exc()
            # Reset buffers and command
            is_recording_command = False
            command_audio_buffer = np.array([], dtype=np.int16)
            command_pause_buffer = np.array([], dtype=np.int16)


def keyword_detected(audio_bytes):
    recognizer = get_stt_recognizer()
    recognizer.AcceptWaveform(audio_bytes)  # 1. Feed audio into the recognizer
    partial = recognizer.PartialResult().lower()  # 2. Read the current partial hypothesis
    print(f"Partial Result: {partial}")
    if config.KEYWORD in partial.lower():
        recognizer.Reset()
        return True

    return False