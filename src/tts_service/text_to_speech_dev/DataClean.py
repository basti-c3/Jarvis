import os

import numpy as np
import soundfile as sf
import whisper
import noisereduce as nr
import simpleaudio as sa
import librosa
from pydub import AudioSegment

from shared.paths import RAW_DATA_DIR_NAME, CLEAN_DATA_DIR_NAME


class DataClean:
    def __init__(self, dir_path, required_sample_rate=22050, whisper_model="base", reduce_noise=False):
        self.transcribe_model = whisper.load_model(whisper_model)
        self.input_path = os.path.join(dir_path, RAW_DATA_DIR_NAME)
        self.output_path = os.path.join(dir_path, CLEAN_DATA_DIR_NAME)
        self.output_wavs_path = os.path.join(self.output_path, "wavs")

        self.required_sample_rate = required_sample_rate
        self.reduce_noise = reduce_noise

    def run(self):
        self.rename_wavs_sequentially()
        self.preprocess_audios()
        self.review_audio_files()
        self.create_metadata()

    def rename_wavs_sequentially(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input path {self.input_path} does not exist")
        # Get all .wav files
        wav_files = [f for f in os.listdir(self.input_path) if f.lower().endswith('.wav')]
        # First pass: Rename all files to temporary names to avoid conflicts
        temp_files = []
        for i, filename in enumerate(wav_files):
            old_path = os.path.join(self.input_path, filename)
            temp_name = f"temp_{i}.wav"
            temp_path = os.path.join(self.input_path, temp_name)
            os.rename(old_path, temp_path)
            temp_files.append(temp_path)

        # Second pass: Rename temp files to 1.wav, 2.wav, ...
        for i, temp_path in enumerate(temp_files, start=1):
            new_name = f"audio_{i}.wav"
            new_path = os.path.join(self.input_path, new_name)
            os.rename(temp_path, new_path)

        print(f"Renamed {len(wav_files)} files.")

    def preprocess_audios(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input path {self.input_path} does not exist")

        os.makedirs(self.output_wavs_path, exist_ok=True)
        # Get only .wav files and count how many there are
        wav_files = [f for f in os.listdir(self.input_path) if f.lower().endswith('.wav')]
        total = len(wav_files)

        for i in range(1, total + 1):
            filename = f"audio_{i}.wav"
            filepath = os.path.join(self.input_path, filename)
            if os.path.isfile(filepath):
                self.clean_audio(filename)
                self.transcribe(filename)
            else:
                raise Exception(
                    FileNotFoundError(f"{filename} not found. Did you call rename_wavs_sequentially before?"))

    def clean_audio(self, filename):
        file_input_path = os.path.join(self.input_path, filename)
        file_output_path = os.path.join(self.output_wavs_path, filename)

        audio_sample, sample_rate = librosa.load(file_input_path, sr=None)

        # Convert to mono
        if audio_sample.ndim > 1:
            audio_sample = librosa.to_mono(audio_sample)

        # Resample
        if sample_rate != self.required_sample_rate:
            audio_sample = librosa.resample(audio_sample, orig_sr=sample_rate, target_sr=self.required_sample_rate)
            sample_rate = self.required_sample_rate

        # Trim silence
        audio_trimmed, _ = librosa.effects.trim(audio_sample, top_db=30)

        # Noise reduction (basic)
        if self.reduce_noise:
            audio_trimmed = nr.reduce_noise(y=audio_trimmed, sr=sample_rate)

        # Normalize
        audio_normalized = audio_trimmed / max(abs(audio_trimmed))

        # 🔊 Add silence padding (e.g., 0.25 seconds on each side)
        pad_duration_sec = 0.25
        pad_samples = int(pad_duration_sec * sample_rate)
        silence = np.zeros(pad_samples)

        audio_padded = np.concatenate([silence, audio_normalized, silence])

        # Save
        sf.write(file_output_path, audio_padded, sample_rate)

    def transcribe(self, filename):
        file_input_path = os.path.join(self.input_path, filename)

        if not os.path.isfile(file_input_path):
            raise FileNotFoundError(f"Audio file not found: {file_input_path}")
        if not file_input_path.endswith(".wav"):
            raise ValueError("Input file must be a .wav file")

        # Transcribe audio
        result = self.transcribe_model.transcribe(file_input_path)
        transcript = result["text"].strip()

        # Save transcript next to the audio file
        filename_without_extension = "".join(filename.split('.')[:-1])
        transcript_path = os.path.join(self.output_wavs_path, filename_without_extension + '.txt')

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"Transcript saved to: {transcript_path}")
        return transcript

    def review_audio_files(self):
        def play_audio(file_path):
            try:
                wave_obj = sa.WaveObject.from_wave_file(file_path)
                play_obj = wave_obj._play()
                play_obj.wait_done()
            except Exception as e:
                print(f"Error playing {file_path}: {e}")

        def load_transcript(txt_path):
            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8") as f:
                    return f.read().strip()
            raise FileNotFoundError(f"transcript path {txt_path} does not exist")

        def save_updated_transcript(txt_path, transcript):
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(transcript.strip())

        wav_files = [f for f in os.listdir(self.output_wavs_path) if f.endswith(".wav")]
        wav_files.sort()

        for wav_file in wav_files:
            wav_path = os.path.join(self.output_wavs_path, wav_file)
            txt_path = os.path.splitext(wav_path)[0] + ".txt"

            print("\n----------------------------------")
            print(f"Now playing: {wav_file}")
            transcript = load_transcript(txt_path)
            print(f"Current transcript: \"{transcript}\"")

            # Play the audio
            play_audio(wav_path)

            updated = False
            while not updated:
                # Get user input
                user_input = input("Enter correction, press Enter to keep, or enter KILL to delete audio: ").strip()

                if user_input == "KILL":
                    os.remove(wav_path)
                    os.remove(txt_path)
                    updated = True
                elif user_input == "REP":
                    play_audio(wav_path)
                elif user_input:
                    save_updated_transcript(txt_path, user_input)
                    print("✅ Transcript updated.")
                    updated = True
                else:
                    print("✅ Transcript accepted unchanged.")
                    updated = True

    def create_metadata(self, output_file="metadata.csv"):
        if not os.path.exists(self.output_path):
            raise FileNotFoundError(f"Cannot create metadata file, output_path {self.output_path} does not exist")

        entries = []
        for file in os.listdir(self.output_wavs_path):
            if file.endswith(".wav"):
                base = os.path.splitext(file)[0]
                txt_path = os.path.join(self.output_wavs_path, f"{base}.txt")
                if os.path.exists(txt_path):
                    with open(txt_path, "r", encoding="utf-8") as f:
                        text = f.read().strip()
                    entries.append(f"{base}||{text}")
                    os.remove(txt_path)

        with open(os.path.join(self.output_path, output_file), "w", encoding="utf-8") as f:
            f.write("\n".join(entries))
        print(f"Created {output_file} with {len(entries)} entries.")

    def transform_files(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        file_list = os.listdir(self.input_path).copy()  # removing while iterating would be bad
        for filename in file_list:
            file_path = os.path.join(self.input_path, filename)

            if filename.endswith('.ogg'):
                new_filename = filename.split('.')[0] + '.wav'
                new_file_path = os.path.join(self.input_path, new_filename)
                self.convert_to_wav(file_path, new_file_path)
                filename = new_filename
                file_path = new_file_path

            if filename.endswith(('.wav', '.flac')):
                y, sr = librosa.load(file_path, sr=22050)

                # trim silence
                trimmed_audio, _ = librosa.effects.trim(y, top_db=30)

                # normalize audio
                normalized_audio = librosa.util.normalize(trimmed_audio)

                output_file_path = os.path.join(self.output_path, filename)
                sf.write(output_file_path, normalized_audio, int(sr), subtype="PCM_16")  # wav
                print(f"Finished file \"{os.path.join(self.output_path, filename)}\"")

    def convert_to_wav(self, audio_file_path, wav_path):
        audio = AudioSegment.from_ogg(audio_file_path)
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(self.required_sample_rate)
        audio.export(wav_path, format="wav")
        print(f"Converted audio file saved as: {wav_path}")
        os.remove(audio_file_path)
        print("Removed old file.")
