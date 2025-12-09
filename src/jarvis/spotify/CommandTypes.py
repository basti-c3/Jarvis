from enum import Enum


class PlayType(Enum):
    track = "song"
    artist = "artist"
    playlist = "playlist"
    album = "album"


class CommandType(Enum):
    stop = "stop"
    skip = "skip"
    continue_playing = "play"
    repeat = "repeat"
    stop_repeat = "stop_repeat"


play_types = [item.value for item in PlayType]
basic_commands = [item.value for item in CommandType]
