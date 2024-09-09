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


def extract_artist_from_search_string(search_str):
    """
        Input:  "hello from adele" / "the lazy song from bruno mars"
        Output: --> ("hello", "adele") / ("the lazy song", "bruno mars")
    """
    split_word = ' from '  # Including the blanks
    if search_str.count(split_word) >= 1:
        # Split only once from the right (also if multiple 'from')
        [track_str, artist_str] = search_str.rsplit(split_word, 1)
        return track_str, artist_str
    else:
        # If no from in search_string no splitting
        return search_str


def normalize_whitespacing(search_str):
    return ' '.join([word for word in search_str.split(' ') if word])
