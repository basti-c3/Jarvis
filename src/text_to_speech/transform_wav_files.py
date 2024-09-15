import os

import librosa
import soundfile as sf
import shutil
import taglib
from pydub import AudioSegment


def update_metadata(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    how_many_files = len(os.listdir(input_folder))

    for i in range(1, how_many_files + 1):
        input_file = os.path.join(input_folder, f"audio_{i}.wav")
        output_file = os.path.join(output_folder, f"audio_{i}.wav")

        if os.path.exists(input_file):
            # Load WAV file and update metadata
            with taglib.File(input_file) as audio:
                # Set the title to match the file name without the extension
                audio.tags["TITLE"] = [f"audio_{i}"]
                # Set the track number to match the file name without the extension
                audio.tags["TRACKNUMBER"] = [f"audio_{i}"]

                # Save updated WAV file
                audio.save()

            # Copy the updated file to the output folder instead of moving it
            shutil.copy2(input_file, output_file)

            print(f"Updated metadata for audio_{i}.wav: title='audio_{i}', track number=audio_{i}")
        else:
            print(f"File {input_file} not found.")


def convert_to_wav(audio_file_path, wav_path):
    audio = AudioSegment.from_ogg(audio_file_path)
    audio = audio.set_channels(1)
    audio = audio.set_sample_width(2)
    audio = audio.set_frame_rate(16000)
    audio.export(wav_path, format="wav")
    print(f"Converted audio file saved as: {wav_path}")
    os.remove(audio_file_path)
    print("Removed old ogg file.")


def transform_files(input_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    file_list = os.listdir(input_path).copy()  # removing while iterating would be bad
    for filename in file_list:
        file_path = os.path.join(input_path, filename)

        if filename.endswith('.ogg'):
            new_filename = filename.split('.')[0] + '.wav'
            new_file_path = os.path.join(input_path, new_filename)
            convert_to_wav(file_path, new_file_path)
            filename = new_filename
            file_path = new_file_path

        if filename.endswith('.wav'):
            y, sr = librosa.load(file_path, sr=16000)

            # trim silence
            trimmed_audio, _ = librosa.effects.trim(y, top_db=30)

            # normalize audio
            normalized_audio = librosa.util.normalize(trimmed_audio)

            output_file_path = os.path.join(output_path, filename)
            sf.write(output_file_path, normalized_audio, int(sr), subtype="PCM_16")


def to_flac():  # needed by vctk training process instead of wav files
    import os
    import re
    from pydub import AudioSegment

    # Path to the directory containing the wav files
    directory = "Basti_audio/wav48_silence_trimmed/basti"

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        # Check if the file is a .wav file and matches the 'audio_x' pattern
        if filename.endswith(".wav") and re.match(r'audio_\d+', filename):
            # Extract the number from the filename using regex
            number = re.findall(r'\d+', filename)[0]

            # Pad the number with leading zeros to make it 3 digits
            new_number = number.zfill(3)

            # Create the new filename in the format 'basti_xxx.flac'
            new_filename = f"basti_{new_number}_mic1.flac"

            # Build full file paths
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)

            # Load the .wav file and convert it to .flac using pydub
            audio = AudioSegment.from_wav(old_file_path)
            audio.export(new_file_path, format="flac")

            # Optionally, delete the original .wav file after conversion
            os.remove(old_file_path)

            print(f"Converted and renamed {filename} to {new_filename}")

    print("All files have been converted and renamed successfully!")


if __name__ == "__main__":
    # transforms all ogg or wav files of the given input_path into wav files of 16000 sample rate to output_path
    input_path = "C:\\Users\\basti\\Documents\\Jarvis\\data\\voice_conversion\\Basti\\training\\original_audio"
    intermediate_path = "C:\\Users\\basti\\Documents\\Jarvis\\data\\voice_conversion\\Basti\\training\\intermediate_audio"
    output_path = "C:\\Users\\basti\\Documents\\Jarvis\\data\\voice_conversion\\Basti\\training\\wavs"

    transform_files(input_path, intermediate_path)
    update_metadata(intermediate_path, output_path)
    print("All .wav files have been processed and saved to the output folder.")
