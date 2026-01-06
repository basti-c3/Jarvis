import queue
import traceback

import numpy as np
from collections import deque

import shared.stt_config as config
from jarvis.core.QuitJarvis import QuitJarvis
from jarvis.core.play_wakeword_sound import play_wakeword_sound
from jarvis.core.process_command import record_command
from jarvis.paths import JARVIS_AWAKEN_PATH, JARVIS_SHUTDOWN_PATH
from shared.Jarvis import jarvis
from shared.stop_event import stop_event
from shared.utils import Warn, STOP_SIGNAL
from jarvis.utils import play_audio_file


def continuous_processing(test_command=None):
    """
        Continuously process audio data from the queue and perform speech recognition
        to detect if a command is coming in.
     """

    is_recording_command = False
    ignore_initial_pause_time = 0 # Set at keyword detection
    detected_silence_time = 0
    command_audio_buffer = np.array([], dtype=np.int16)
    pre_roll_buffer = deque(maxlen=config.PRE_ROLL_SAMPLES)

    if test_command:
        is_recording_command = True

    while not stop_event.is_set():
        try:
            # Get audio data from the queue
            audio_queue = jarvis.audio_queue
            audio_chunk = audio_queue.get(timeout=1)  # Get audio data from the queu
            pre_roll_buffer.extend(audio_chunk)

            if ignore_initial_pause_time > 0:
                # Skip counting silence for the initial assistant audio
                ignore_initial_pause_time -= config.BUFFER_DURATION
                detected_silence_time = 0
            elif np.mean(np.abs(audio_chunk)) < config.SILENCE_THRESHOLD:
                detected_silence_time += config.BUFFER_DURATION
            else:
                detected_silence_time = 0

            if not is_recording_command:
                keyword_index = jarvis.wake_word.process(audio_chunk)

                if keyword_index >= 0:
                    print("Wake word detected!")
                    play_wakeword_sound(str(JARVIS_AWAKEN_PATH))
                    is_recording_command = True

                    # How long the assistant audio is (in seconds)
                    ignore_initial_pause_time = config.INITIAL_PAUSE_TIME  # adjust to length of your "Yes?" sound

                    # Include pre-roll audio
                    command_audio_buffer = np.fromiter(
                        pre_roll_buffer, dtype=np.int16
                    )

                if not is_recording_command and detected_silence_time >= config.RESET_AUDIO_BUFFER_AFTER:
                    detected_silence_time = 0
                    pre_roll_buffer.clear()
                    command_audio_buffer = np.array([], dtype=np.int16)
            else:
                try:
                    command_finished, command_audio_buffer = record_command(command_audio_buffer,
                                                                                                  audio_chunk.flatten(),
                                                                                                  detected_silence_time,
                                                                                                  test_command)
                except QuitJarvis:
                    raise KeyboardInterrupt()
                except Exception as error:
                    command_finished = True  # Reset buffers after error to start anew
                    Warn(str(error))
                    jarvis.say("Sorry Sir, but something went terribly wrong here, please try again.")
                finally:
                    if command_finished:
                        # Reset buffers and command
                        is_recording_command = False
                        pre_roll_buffer.clear()
                        command_audio_buffer = np.array([], dtype=np.int16)
        except queue.Empty:
            continue  # Continue if the queue is empty
        except KeyboardInterrupt:
            play_audio_file(JARVIS_SHUTDOWN_PATH, jarvis.audio_device_sample_rate)
            jarvis.stt_service_client.send(STOP_SIGNAL.encode("utf-8"))
            jarvis.tts_service_client.send_string(STOP_SIGNAL)
            print("Jarvis stopped.")
            break
        except Exception as e:
            print(f"Error recognizing vosk_model: {e}")
            traceback.print_exc()
            # Reset buffers and command
            is_recording_command = False
            command_audio_buffer = np.array([], dtype=np.int16)
