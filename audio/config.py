# Settings for the audio input
import pyaudio

CHUNK = 1024  # Buffer size
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono audio
RATE = 16000  # Sampling rate
OVERLAP_SIZE = int(0.5 * RATE)  # 0.5 seconds overlap size
AUDIO_CHUNK_LENGTH = 3  # seconds length of audio material listened to for the word Jarvis
MAX_COMMAND_LENGTH = 20  # maximum seconds of commands
COMMAND_END_PAUSE_LENGTH = 1  # length of pause to stop a command
KEYWORD = "jarvis".lower()  # make sure it is lower case!
PAUSE_THRESHOLD = 0.01  # mean energy level threshold to detect a pause

DEV = True
