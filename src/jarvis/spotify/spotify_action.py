from shared.Jarvis import jarvis
from spotify.ResponseError import ResponseError
from spotify.spotify_utils import raise_spotify_response_error


def spotify_action(success_message: str = None):
    """Decorator to wrap Spotify commands with uniform error handling."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                if success_message:
                    jarvis.say(success_message)
                return result
            except ResponseError as error:
                raise_spotify_response_error(error.args[0])
        return wrapper
    return decorator
