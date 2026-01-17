from jarvis.Jarvis import jarvis


class TestCreatingAudioOutput:
    """Tests for speaking of Jarvis, so giving a text and creating audio output."""

    def test_speak(self):
        """Tests speaking."""

        jarvis.say("This is a test phrase!")
