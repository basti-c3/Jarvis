def Warn(message, *args):
    # This prints a warning in red color into the terminal without breaking the code at the point of the warning
    if args:  # Checks if args is not empty
        print("\033[91m" + message + " " + str(args) + "\033[0m")
    else:
        print("\033[91m" + message + "\033[0m")


spotify_base_url = "https://api.spotify.com/v1"
spotify_token_url = "https://accounts.spotify.com/api/token"
spotify_redirect_url = 'http://localhost:3000/callback'
spotify_auth_url = 'https://accounts.spotify.com/authorize'
