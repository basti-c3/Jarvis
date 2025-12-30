import os

from shared.Jarvis import jarvis
from shared.utils import Warn

MQTT_BROKER = os.getenv('MQTT_BROKER')  # Replace with your Mosquitto broker IP
MQTT_PORT = int(os.getenv('MQTT_PORT'))  # Default MQTT port
MQTT_USER = os.getenv('MQTT_USER')  # MQTT username (if set)
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')  # MQTT password

PLUG_LICHTERKETTE_TOPIC = "plug_lichterkette_1"  # 1
PLUG_LAMPE_TOPIC = "plug_lampe_2"  # 2
PLUG_FERNSEHER_TOPIC = "plug_fernseher_3"  # 3
PLUG_KUECHE_TOPIC = "plug_kueche_4"  # 4

BULB_1 = "bulb_1"
BULB_2 = "bulb_2"
BULB_3 = "bulb_3"


def raise_mqtt_response_error(error_response):
    Warn(f"Mqtt: Failed to do something , status: {error_response.status_code} {error_response.reason}")
    jarvis.say(
        "Sorry, Sir. I encountered a problem executing the requested command to the MQTT devices. The response was not as expected.")
