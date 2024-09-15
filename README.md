# Jarvis

## Description
Welcome to our project! This is a a try to create JARVIS model in Python. 

## Contributing
We welcome any and all contributions! Here are some ways you can get started:
1. Report bugs: If you encounter any bugs, please let us know. Open up an issue and let us know the problem.
2. Contribute code: If you are a developer and want to contribute, follow the instructions below to get started!
3. Suggestions: If you don't want to code but have some awesome ideas, open up an issue explaining some updates or imporvements you would like to see!
4. Documentation: If you see the need for some additional documentation, feel free to add some!

## TODOs


## Common errors:
- AttributeError: 'TTS' object has no attribute 'is_multi_lingual' 
--> change in TTS/api.py property is_multi_lingual (see https://github.com/coqui-ai/TTS/issues/3449) to:
@property
def is_multi_lingual(self):
    if hasattr(self.synthesizer.tts_model, "language_manager") and self.synthesizer.tts_model.language_manager:
        return self.synthesizer.tts_model.language_manager.num_languages > 1
    if (
            isinstance(self.model_name, str)
            and "xtts" in self.model_name
            or self.config
            and "xtts" in self.config.model
    ):
        return True
    return False
