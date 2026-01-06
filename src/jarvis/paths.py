from pathlib import Path

spotify_base_url = "https://api.spotify.com/v1"
spotify_token_url = "https://accounts.spotify.com/api/token"
spotify_redirect_url = 'http://localhost:3000/callback'
spotify_auth_url = 'https://accounts.spotify.com/authorize'
BASE_DIR: Path = Path(__file__).resolve().parents[2]
SRC_DIR: Path = BASE_DIR / "src"
WAKE_WORD_PATH: Path = SRC_DIR / "jarvis" / "settings/Jarvis_en_windows_v4_0_0.ppn"
PRECAL_AUDIOS_PATH: Path = BASE_DIR / "data/precalculated_jarvis_audios"
JARVIS_AWAKEN_PATH: Path = PRECAL_AUDIOS_PATH / "yes.wav"
JARVIS_SHUTDOWN_PATH: Path = PRECAL_AUDIOS_PATH / "shuttingdowngoodbyesir.wav"
RESOURCE_DIR: Path = BASE_DIR / "src" / "resources"
SPOTIFY_TOKEN_DIR_PATH = str(RESOURCE_DIR / "spotify_tokens")
STT_MODEL_PATH = str(BASE_DIR / "models" / "vosk-model-small-en-us-0.15")

# Config
env_config_path = lambda env: str(BASE_DIR / f"config/{env}-env.yml")

# TTS
METADATA_FILENAME = 'metadata.csv'
RAW_DATA_DIR_NAME = 'raw_test_data'
CLEAN_DATA_DIR_NAME = 'cleaned_test_data'
VITS_MODEL_PATH = "C:/Users/basti/AppData/Local/tts/tts_models--en--ljspeech--vits/model_file.pth"
VITS_CONFIG_PATH = "C:/Users/basti/AppData/Local/tts/tts_models--en--ljspeech--vits/config.json"
XTTS_MODEL_PATH = "tts_models/multilingual/multi-dataset/xtts_v2"
DEFAULT_OUT_TEXT = "This is a generic text to be translated by this amazing new voice for testing purposes."
