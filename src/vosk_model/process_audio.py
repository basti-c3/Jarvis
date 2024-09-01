import queue
import traceback

import src.vosk_model.config as config
from src.vosk_model.global_vars import audio_queue
from src.vosk_model.speech_to_text import recognizer


def process_audio():
    """
        Continuously process vosk_model data from the queue and perform speech recognition
        to detect if a command is coming in.
     """
    print("Listening for the word 'Jarvis'...")

    is_recording_command = False

    while True:
        try:
            # Get vosk_model data from the queue
            audio_chunk = audio_queue.get(timeout=1)  # Get vosk_model data from the queue
            if recognizer.AcceptWaveform(audio_chunk.tobytes()):
                result = recognizer.Result()
                if config.KEYWORD in result.lower():
                    print("Keyword 'Jarvis' detected!")
                    # is_recording_command = True

            else:
                partial_result = recognizer.PartialResult()
                print(f"Partial Result: {partial_result}")
                if config.KEYWORD in partial_result.lower():
                    print("Keyword 'Jarvis' detected in partial result!")
                    # is_recording_command = True
        except queue.Empty:
            continue  # Continue if the queue is empty
        except Exception as e:
            print(f"Error recognizing vosk_model: {e}")
            traceback.print_exc()
