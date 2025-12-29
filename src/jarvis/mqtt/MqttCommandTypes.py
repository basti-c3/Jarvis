from enum import Enum


class MqttCommandType(Enum):
    kitchen_toggle = "kitchen_toggle"
    kitchen_on = "kitchen_on"
    kitchen_off = "kitchen_off"
    lights_on = "lights_on"
    lights_off = "lights_off"
    cozy = "cozy"


mqtt_basic_commands = [item.value for item in MqttCommandType]
