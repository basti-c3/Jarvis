import sounddevice as sd


def Warn(message, *args):
    # This prints a warning in red color into the terminal without breaking the code at the point of the warning
    if args:  # Checks if args is not empty
        print("\033[91m" + str(message) + " " + str(args) + "\033[0m")
    else:
        print("\033[91m" + str(message) + "\033[0m")


STOP_SIGNAL: str = "protocol suicide"


def find_anker_usb_mic(name_substring="Anker"):
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0 and name_substring.lower() in dev['name'].lower():
            return i, dev['default_samplerate']
    return None, None
