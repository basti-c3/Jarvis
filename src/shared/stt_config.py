# Settings for the vosk input
from vosk import SetLogLevel

KEYWORD = "jarvis".lower()  # make sure it is lower case!

BUFFER_DURATION = 0.032  # Duration of each buffer in seconds
AUDIO_RATE = 16000  # Sampling rate should be 16000 Hz for vosk
CHANNELS = 1  # Mono vosk for vosk
MAX_COMMAND_LENGTH = 20  # maximum seconds of commands
COMMAND_END_PAUSE_LENGTH = 1  # length of pause to stop a command
RESET_AUDIO_BUFFER_AFTER = 2
SILENCE_THRESHOLD = 0.0025 * 32767  # mean energy level threshold to detect a pause (the 32767 because of int16 format)
PRE_ROLL_SECONDS = 2.5  # tuneable
PRE_ROLL_SAMPLES = int(PRE_ROLL_SECONDS * AUDIO_RATE)
INITIAL_PAUSE_TIME = 2
DEV = True
SetLogLevel(-1)  # To remove all the annoying logs
