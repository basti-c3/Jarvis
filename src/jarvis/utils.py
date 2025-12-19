import platform
import winsound


def Warn(message, *args):
    # This prints a warning in red color into the terminal without breaking the code at the point of the warning
    if args:  # Checks if args is not empty
        print("\033[91m" + str(message) + " " + str(args) + "\033[0m")
    else:
        print("\033[91m" + str(message) + "\033[0m")


def play_audio(filename):
    filepath = f"../../data/precalculated_jarvis_audios/{filename}.wav"
    if platform.system() == "Windows":
        # Uses built-in Windows sound player
        winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        raise SystemError("Please configure playing audio for non-windows systems before running the code")