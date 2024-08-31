from audio import config
from audio.speech_to_text import speech_to_text


def process_command(audio):
    if config.DEV:
        result_command = speech_to_text(audio)
    else:
        result_command = speech_to_text(audio, "large")
    print("--------------------------------------------------------")
    print(f"Recognized Command: {result_command['text']}")

    result_txt = result_command['text']
    result_txt_lower = result_txt.lower()
    keyword_index = result_txt_lower.find(config.KEYWORD)
    if keyword_index != -1:
        # Calculate the starting position of the text after the keyword
        start_index = keyword_index + len(config.KEYWORD)

        # Slice the string to get the text after the keyword
        text_after_keyword = result_txt[start_index:].strip()

        print(f"Text following the keyword '{config.KEYWORD}': {text_after_keyword}")

        if 'turtle' in text_after_keyword.lower():
            print("Turtle recognized!!!")
    else:
        print(f"The keyword '{config.KEYWORD}' was not found in the text.")
