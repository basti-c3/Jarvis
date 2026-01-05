from jarvis.settings.config_loader import load_config


def main():
    config = load_config()
    print(f"Running Jarvis in {config.get('mode', 'unknown')} mode.")

    from jarvis.core.runner import run_recognition
    run_recognition()


if __name__ == "__main__":
    main()
