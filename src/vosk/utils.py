def Warn(message, *args):
    # This prints a warning in red color into the terminal without breaking the code at the point of the warning
    if args:  # Checks if args is not empty
        print("\033[91m" + message + " " + str(args) + "\033[0m")
    else:
        print("\033[91m" + message + "\033[0m")