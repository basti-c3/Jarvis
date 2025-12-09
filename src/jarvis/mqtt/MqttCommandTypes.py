from enum import Enum


class MqttCommandType(Enum):
    lights_on = "lights_on"
    lights_off = "lights_off"


mqtt_basic_commands = [item.value for item in MqttCommandType]
