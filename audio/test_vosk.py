import os
import wave
import json
from vosk import Model, KaldiRecognizer

# Path to your Vosk model directory
model_path = "../models/vosk-model-small-en-us-0.15"

# Load the Vosk model
if not os.path.exists(model_path):
    print(
        f"Please download the model from https://alphacephei.com/vosk/models and unpack as '{model_path}' in the current folder.")
    exit(1)

model = Model(model_path)

# Open the audio file you want to transcribe
wav_file_path = "../music_text.wav"

# Ensure your audio file is in the correct format (Mono PCM WAV format)
wf = wave.open(wav_file_path, "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Audio file must be WAV format mono PCM.")
    exit(1)

# Initialize the recognizer with the model and sample rate
recognizer = KaldiRecognizer(model, wf.getframerate())

# Initialize an empty string to accumulate the recognized text
recognized_text = ""

# Process the audio file in chunks
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result_text = json.loads(result).get('text', '')
        recognized_text += result_text + " "  # Accumulate recognized text
    else:
        partial_result = recognizer.PartialResult()
        partial_text = json.loads(partial_result).get('partial', '')
        print("Partial text recognized: ", partial_text)
        recognized_text += partial_text + " "  # Accumulate partial text

# Get the final result after processing all chunks
final_result = recognizer.FinalResult()
final_text = json.loads(final_result).get('text', '')
recognized_text += final_text  # Append final result to the accumulated text

# Print the complete recognized text
print("Full Recognized Text:")
print(recognized_text)

# Close the audio file
wf.close()
