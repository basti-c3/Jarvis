import numpy as np

import shared.stt_config as config
from core.transcribe_command import transcribe_command
from mqtt.MqttCommand import MqttCommand
from mqtt.MqttCommandTypes import MqttCommandType
from spotify.SpotifyCommandTypes import SpotifyCommandType

from spotify.SpotifyCommand import SpotifyCommand


def record_command(audio_buffer: np.array, pause_buffer: np.array, new_audio_chunk: np.array, test_command=None):
    print("Recording command...")
    audio_buffer = np.concatenate((audio_buffer, new_audio_chunk))
    pause_buffer = np.concatenate((pause_buffer, new_audio_chunk))

    pause_buffer_long_enough = len(
        pause_buffer) > config.AUDIO_RATE * config.COMMAND_END_PAUSE_LENGTH
    is_end_of_command = pause_buffer_long_enough and np.mean(
        np.abs(pause_buffer)) < config.SILENCE_THRESHOLD

    if pause_buffer_long_enough:
        # Remove the first audio chunk to maintain the same length of the pause_buffer_long_enough
        pause_buffer = pause_buffer[len(new_audio_chunk):]

    command_length_exceeded = len(audio_buffer) > config.AUDIO_RATE * config.MAX_COMMAND_LENGTH
    if is_end_of_command or command_length_exceeded:
        if is_end_of_command:
            print("Detected pause in speech. Ending command capture...")
        else:
            print(f"Maximum command length of {config.MAX_COMMAND_LENGTH} was reached. Ending command capture...")
        if test_command is None:
            command_str = transcribe_command(audio_buffer)
            print(f"Command: {command_str}")
        else:
            command_str = test_command

        if command_str is not None:
            process_command(command_str)  # Process command
        return True, audio_buffer, pause_buffer
    return False, audio_buffer, pause_buffer


def process_command(command_str):
    command_str = command_str.lower()

    if 'play' in command_str \
            or 'stop' in command_str\
            or 'continue' in command_str \
            or 'skip' in command_str\
            or 'repeat' in command_str:
        spotify_command = SpotifyCommand(command_str=command_str)

        # If a string is not found, find returns -1
        # Check order of keywords (e.g. either "stop playing" vs "play please don't stop the music")
        kw_before_play = lambda kw: 0 <= command_str.find(kw) and \
                                    (command_str.find('play') == -1
                                     or command_str.find(kw) < command_str.find('play')
                                     )
        if kw_before_play('stop'):
            spotify_command.type = SpotifyCommandType.stop
        elif kw_before_play('continue') or command_str == 'play':
            spotify_command.type = SpotifyCommandType.continue_playing
        elif kw_before_play('skip'):
            spotify_command.type = SpotifyCommandType.skip
        elif kw_before_play('repeat'):
            if command_str.find('repeat') < command_str.find('off'):
                spotify_command.type = SpotifyCommandType.stop_repeat
            else:
                spotify_command.type = SpotifyCommandType.repeat
        else:  # General play command. Needs to be further processed to extract the exact command
            spotify_command.extract()
        # Command is set / extracted --> execute
        spotify_command.execute()

    elif 'kitchen' in command_str:
        mqtt_command = MqttCommand(command_str=command_str)
        if 'on' in command_str:
            mqtt_command.type = MqttCommandType.kitchen_on
            mqtt_command.execute()
        elif 'off' in command_str:
            mqtt_command.type = MqttCommandType.kitchen_off
            mqtt_command.execute()
        else:
            mqtt_command.type = MqttCommandType.kitchen_toggle
            mqtt_command.execute()
    elif 'good morning' in command_str or 'goodmorning' in command_str:
        mqtt_command = MqttCommand(command_str=command_str)
        mqtt_command.type = MqttCommandType.lights_on
        mqtt_command.execute()
    elif 'good night' in command_str or 'goodnight' in command_str:
        mqtt_command = MqttCommand(command_str=command_str)
        mqtt_command.type = MqttCommandType.lights_off
        mqtt_command.execute()
    elif 'light' in command_str:
        mqtt_command = MqttCommand(command_str=command_str)
        if 'on' in command_str:
            mqtt_command.type = MqttCommandType.lights_on
            mqtt_command.execute()
        elif 'off' in command_str:
            mqtt_command.type = MqttCommandType.lights_off
            mqtt_command.execute()
    elif 'comfortable' in command_str or 'cozy' in command_str:
        mqtt_command = MqttCommand(command_str=command_str)
        mqtt_command.type = MqttCommandType.cozy
        mqtt_command.execute()
