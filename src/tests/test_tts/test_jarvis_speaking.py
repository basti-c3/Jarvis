from unittest.mock import patch


from speech_to_text.process_command import process_command


class TestCreatingAudioOutput:
    """Tests for speaking of Jarvis, so giving a text and creating audio output."""

    def test_speak(self):
        """Tests speaking."""
        from Jarvis import jarvis
        jarvis.say("This is a test phrase!")
