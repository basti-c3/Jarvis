from requests import Response

from shared.Jarvis import jarvis
from shared.utils import Warn


def preprocess_spotify_search_string(command_str):
    """
    Input:  "play hello from adele on spotify" / "play hello from adele"
    Output: --> "hello from adele"
    """

    play_index = command_str.find('play')
    spotify_index = command_str.find('spotify')  # Doesn't have to be in the string necessarily
    spotify_in_command = spotify_index != -1
    if play_index < spotify_index and spotify_in_command:
        extracted_command = command_str[play_index + len('play'):spotify_index].strip()
        # Remove the last word (the one immediately before 'spotify', for example 'on'/'in'/'with'/'from')
        words = extracted_command.split()
        if len(words) > 1:
            words.pop()
            extracted_command = ' '.join(words)
    else:  # spotify is part of the string but before the word play, so just take the words after "play"
        extracted_command = command_str[play_index + len('play'):].strip()
    if 'playlist' in extracted_command and extracted_command.startswith('a '):
        # play a rock music playlist --> rock music playlist / play a beautiful day --> a beautiful day
        extracted_command = extracted_command[2:]  # Remove the starting a
    elif 'playlist' in extracted_command and extracted_command.startswith('my '):
        # play my rock music playlist --> rock music playlist / play my love will never die --> my love will never die
        extracted_command = extracted_command[3:]  # Remove the starting my

    return extracted_command


def extract_artist_from_search_string(search_str: str, split_words: list[str]):
    """
        Input:  "hello from adele" / "the lazy song from bruno mars"
        Output: --> ("hello", "adele") / ("the lazy song", "bruno mars")
    """
    white_spaced_split_words = [f' {word.strip()} ' for word in split_words]
    # Find the rightmost occurrence of any split word
    last_pos = -1
    latest_split_word = None
    for word in split_words:
        pos = search_str.rfind(word)
        if pos > last_pos:
            last_pos = pos
            latest_split_word = word

    if latest_split_word is not None and last_pos != -1:
        track_str, artist_str = search_str.rsplit(latest_split_word, 1)
        return track_str.strip(), artist_str.strip()

    # If no known split word found
    return search_str.strip(), None


def normalize_whitespacing(search_str):
    return ' '.join([word for word in search_str.split(' ') if word])


def print_warning_response_json_if_possible(response: Response):
    try:
        Warn(response.json())
    except Exception:  # If not possible to convert response to json, don't print it
        pass


def raise_spotify_response_error(error_response: Response):
    Warn(f"Spotify: Failed to play , status: {error_response.status_code} {error_response.reason}")
    jarvis.say("Sorry, Sir. I encountered a problem executing the requested command to the Spotify API. The response was not as expected.")
