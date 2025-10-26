import time
from global_init import init_globals
from settings.config_loader import load_config


def main():
    config = load_config()
    print(f"Running Jarvis in {config.get('mode', 'unknown')} mode.")
    print("Loading models...")
    start_time = time.time()

    init_globals()

    model_loading_time = time.time() - start_time
    print(f"Models loaded ({model_loading_time:.2f}s)")

    from speech_to_text.runner import run_recognition
    run_recognition()


if __name__ == "__main__":
    main()
