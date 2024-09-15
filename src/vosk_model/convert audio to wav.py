import os
import wave

from pydub import AudioSegment


def check_properties_of_wav(wav_file_path):  # To see if correct format of wav file
    with wave.open(wav_file_path, 'rb') as wf:
        print(f"Number of Channels: {wf.getnchannels()}")
        print(f"Sample Width: {wf.getsampwidth()}")
        print(f"Sample Rate: {wf.getframerate()}")
        print(f"Compression Type: {wf.getcomptype()}")


def convert_to_wav(audio_file_path, wav_path, type="mp3"):
    if type == "mp3":
        audio = AudioSegment.from_mp3(audio_file_path)
    elif type == "ogg":
        audio = AudioSegment.from_ogg(audio_file_path)
    audio = audio.set_channels(1)
    audio = audio.set_sample_width(2)
    audio = audio.set_frame_rate(16000)
    audio.export(wav_path, format="wav")
    print(f"Converted audio file saved as: {wav_path}")
    check_properties_of_wav(wav_path)


mp3_file_path = "../music_text.ogg"
wav_file_path = "../data/audiofiles/music_text.wav"
#convert_to_wav(mp3_file_path, wav_file_path, "ogg")

direcory_path = "../../data/voice_conversion/Sebastian"
for file in os.listdir(direcory_path):
    if 'ogg' in file:
        file_path = os.path.join(direcory_path, file)
        out_file_path = os.path.join(direcory_path, file.split('.')[0] + '.wav')
        convert_to_wav(file_path, out_file_path, "ogg")
        os.remove(file_path)