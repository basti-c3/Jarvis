from Jarvis import jarvis
from utils import Warn

MQTT_BROKER = "192.168.178.76"  # Replace with your Mosquitto broker IP
MQTT_PORT = 1883  # Default MQTT port
MQTT_USER = "basti"  # MQTT username (if set)
MQTT_PASSWORD = "gdg71U0n3SityGB4TEfo"  # MQTT password

PLUG_LICHTERKETTE_TOPIC = "plug_lichterkette"  # 1
PLUG_LAMPE_TOPIC = "plug_lampe"  # 2
PLUG_FERNSEHER_TOPIC = "plug_fernseher"  # 3
PLUG_KUECHE_TOPIC = "plug_kueche"  # 4


def raise_mqtt_response_error(error_response):
    Warn(f"Mqtt: Failed to do something , status: {error_response.status_code} {error_response.reason}")
    jarvis.say(
        "Sorry, Sir. I encountered a problem executing the requested command to the MQTT devices. The response was not as expected.")
