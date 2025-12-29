import traceback

from paho.mqtt.client import Client

from mqtt.MqttError import MqttError
from mqtt.mqtt_utils import *
from shared.utils import Warn


class MqttDevice:
    client: Client
    topic: str

    def __init__(self, client_id):
        try:
            self.topic = client_id
            self.client = Client(client_id=client_id)
            self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
            self.client.on_connect = self._on_mqtt_connect
            self.client.on_message = self._on_mqtt_message
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
        except Exception as error:
            Warn(error)
            Warn(traceback.format_exc())
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
        pass

    def turn_on(self):
        try:
            self.client.publish(f"cmnd/{self.topic}/POWER", "ON")
        except Exception as error:
            Warn(f"Something went wrong turning on {self.topic}" + error.args[0])
            raise MqttError(error.args[0])

    def turn_off(self):
        try:
            self.client.publish(f"cmnd/{self.topic}/POWER", "OFF")
        except Exception as error:
            Warn(f"Something went wrong turning off {self.topic}" + error.args[0])
            raise MqttError(error.args[0])

    def toggle(self):
        try:
            self.client.publish(f"cmnd/{self.topic}/POWER", "TOGGLE")
        except Exception as error:
            Warn(f"Something went wrong toggling {self.topic}" + error.args[0])
            raise MqttError(error.args[0])
