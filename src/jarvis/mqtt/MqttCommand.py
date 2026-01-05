from jarvis.mqtt.MqttCommandTypes import MqttCommandType
from jarvis.mqtt.MqttService import MqttService


class MqttCommand:
    def __init__(self, command_str=""):
        self.mqtt_service = MqttService()
        self.command_str = command_str.lower()
        self.type = None  # Is set in the extract method

    def execute(self):
        if self.type == MqttCommandType.lights_off:
            self.mqtt_service.turn_off_lights()
        elif self.type == MqttCommandType.lights_on:
            self.mqtt_service.turn_on_lights()
        elif self.type == MqttCommandType.cozy:
            self.mqtt_service.make_it_cozy()
        elif self.type == MqttCommandType.kitchen_on:
            self.mqtt_service.turn_kitchen_plug_on()
        elif self.type == MqttCommandType.kitchen_off:
            self.mqtt_service.turn_kitchen_plug_off()
        elif self.type == MqttCommandType.kitchen_toggle:
            self.mqtt_service.kitchen_plug_toggle()
