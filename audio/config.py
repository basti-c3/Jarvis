# Settings for the audio input
import pyaudio
from vosk import SetLogLevel

BUFFER_DURATION = 0.5  # Duration of each buffer in seconds
AUDIO_RATE = 16000  # Sample rate in Hz


CHUNK = 1024  # Buffer size
FORMAT = pyaudio.paInt16  # 16-bit resolution for vosk
CHANNELS = 1  # Mono audio for vosk
RATE = 16000  # Sampling rate should be 16000 for vosk
OVERLAP_SIZE = int(0.5 * RATE)  # 0.5 seconds overlap size
AUDIO_CHUNK_LENGTH = 3  # seconds length of audio material listened to for the word Jarvis
MAX_COMMAND_LENGTH = 20  # maximum seconds of commands
COMMAND_END_PAUSE_LENGTH = 1  # length of pause to stop a command
KEYWORD = "jarvis".lower()  # make sure it is lower case!
SILENCE_THRESHOLD = 0.01 * 32767  # mean energy level threshold to detect a pause (the 32767 because of int16 format)

DEV = True
SetLogLevel(-1)  # To remove all the annoying logs
