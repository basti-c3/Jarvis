from unittest.mock import patch
from speech_to_text.process_command import process_command


class TestMqttBasicCommand:
    """Pytest-style tests for MqttCommand basic commands."""

    def test_turn_on_lights(self):
        """Tests that turn on the light bulbs."""
        import mqtt.MqttService as mqtt_service
        # Get the method object directly from the class
        with patch.object(mqtt_service.MqttService, "turn_on_lights") as mock_turn_on_lights:
            process_command("Jarvis, good Morning")
            mock_turn_on_lights.assert_called_once_with()

        process_command("Jarvis, good Morning")


    def test_turn_off_lights(self):
        """Tests that turn off the light bulbs."""
        import mqtt.MqttService as mqtt_service
        # Get the method object directly from the class

        with patch.object(mqtt_service.MqttService, "turn_off_lights") as mock_turn_off_lights:
            process_command("Jarvis, good night")
            mock_turn_off_lights.assert_called_once_with()

        process_command("Jarvis, good night")

