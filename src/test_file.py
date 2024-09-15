import os

# Define the directory where the audio files are located
directory_path = "../data/voice_conversion/Basti/training/original_audio"

# Loop through all files in the directory
for file_name in os.listdir(directory_path):
    # Check if the file name matches the pattern "audio_ (x).wav"
    if file_name.startswith("audio_ (") and file_name.endswith(".wav"):
        # Create the new file name by removing the space between the underscore and the number
        new_file_name = file_name.replace("audio_ (", "audio_").replace(").wav", ".wav")

        # Get the full paths for renaming
        old_file_path = os.path.join(directory_path, file_name)
        new_file_path = os.path.join(directory_path, new_file_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {file_name} -> {new_file_name}')
