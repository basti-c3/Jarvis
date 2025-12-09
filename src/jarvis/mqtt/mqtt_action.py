from Jarvis import jarvis
from mqtt.MqttError import MqttError
from mqtt.mqtt_utils import raise_mqtt_response_error


def mqtt_action(success_message: str = None):
    """Decorator to wrap MQTT commands with uniform error handling."""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                if success_message:
                    jarvis.say(success_message)
                return result
            except MqttError as error:
                raise_mqtt_response_error(error.args[0])

        return wrapper

    return decorator
