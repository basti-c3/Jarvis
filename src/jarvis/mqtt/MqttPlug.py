from paho.mqtt.client import Client

from mqtt.MqttError import MqttError
from mqtt.mqtt_utils import *
from utils import Warn


class MqttPlug:
    client: Client
    topic: str
    is_a_light: bool

    def __init__(self, client_id, is_a_light):
        try:
            self.topic = client_id
            self.is_a_light = is_a_light
            self.client = Client(client_id=client_id)
            self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
            self.client.on_connect = self._on_mqtt_connect
            self.client.on_message = self._on_mqtt_message
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
        except Exception as error:
            Warn(error.args[0])
            self._on_mqtt_disconnect()

    # Mqtt Connect callback
    def _on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected {self.topic} to MQTT Broker!")
        else:
            Warn(f"Failed to connect, return code {rc}")

    def _on_mqtt_disconnect(self):
        try:
            # Disconnect when done
            self.client.loop_stop()
            self.client.disconnect()
        except Exception:
            pass  # Ignore exceptions on disconnect

    # Optional: receive messages from the plug
    def _on_mqtt_message(self, client, userdata, msg):
        pass  # Todo: Complaining jarvis that you should use him to turn it on

    def turn_on(self):
        try:
            self.client.publish(f"cmnd/{self.topic}/POWER", "ON")
        except Exception as error:
            Warn(f"Something went wrong turning on the lights of {self.topic}" + error.args[0])
            raise MqttError(error.args[0])

    def turn_off(self):
        try:
            self.client.publish(f"cmnd/{self.topic}/POWER", "OFF")
        except Exception as error:
            Warn(f"Something went wrong turning off the lights of {self.topic}" + error.args[0])
            raise MqttError(error.args[0])

    def toggle(self):
        try:
            self.client.publish(f"cmnd/{self.topic}/POWER", "TOGGLE")
        except Exception as error:
            Warn(f"Something went wrong toggling the lights of {self.topic}" + error.args[0])
            raise MqttError(error.args[0])
