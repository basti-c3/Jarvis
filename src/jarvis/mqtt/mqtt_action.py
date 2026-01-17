from jarvis.mqtt.MqttError import MqttError
from jarvis.mqtt.mqtt_utils import raise_mqtt_response_error
from jarvis.Jarvis import jarvis
from shared.utils import Warn


def mqtt_action(success_message: str = None):
    """Decorator to wrap MQTT commands with uniform error handling."""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                if success_message:
                    try:
                        jarvis.say(success_message)
                    except Exception as error:
                        Warn(f"ERROR in jarvis speaking: {str(error)}")
                return result
            except MqttError as error:
                raise_mqtt_response_error(error.args[0])

        return wrapper

    return decorator
