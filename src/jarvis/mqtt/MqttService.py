from global_init import *
from mqtt.mqtt_action import mqtt_action


class MqttService:
    def __init__(self):
        self.plug_lichterkette = get_plug_lichterkette()
        self.plug_lampe = get_plug_lampe()
        self.plug_fernseher = get_plug_fernseher()
        self.plug_kueche = get_plug_kueche()
        self.all_plugs = [self.plug_lichterkette, self.plug_lampe, self.plug_fernseher, self.plug_kueche]

    @mqtt_action("Turning off the lights. Good night, Sir!")
    def turn_off_lights(self):
        for plug in self.all_plugs:
            plug.turn_off()

    @mqtt_action("Turning on the lights. Good morning, Sir!")
    def turn_on_lights(self):
        for plug in self.all_plugs:
            plug.turn_on()
