from shared.global_init import *
from mqtt.mqtt_action import mqtt_action


class MqttService:
    def __init__(self):
        self.plug_lichterkette = get_plug_lichterkette()
        self.plug_lampe = get_plug_lampe()
        self.plug_fernseher = get_plug_fernseher()
        self.plug_kueche = get_plug_kueche()
        self.all_plugs = [self.plug_lichterkette, self.plug_lampe, self.plug_fernseher, self.plug_kueche]
        self.all_bulbs = get_light_bulbs()

    @mqtt_action("Turning off the lights. Good night, Sir!")
    def turn_off_lights(self):
        for plug in self.all_plugs:
            if plug.is_a_light:
                plug.turn_off()
        for bulb in self.all_bulbs:
            bulb.turn_off()

    @mqtt_action("Turning on the lights. Good morning, Sir!")
    def turn_on_lights(self):
        for bulb in self.all_bulbs:
            bulb.turn_on()
            bulb.lights_to_normal()

    @mqtt_action("Enjoy a comfortable evening!")
    def make_it_cozy(self):
        for plug in self.all_plugs:
            if plug.is_a_light:
                plug.turn_off()
        for bulb in self.all_bulbs:
            bulb.turn_off()

        self.plug_lichterkette.turn_on()

    @mqtt_action("Of course, here you go!")
    def turn_kitchen_plug_on(self):
        self.plug_kueche.turn_on()

    @mqtt_action("Of course, here you go!")
    def turn_kitchen_plug_off(self):
        self.plug_kueche.turn_off()

    @mqtt_action("Of course, here you go!")
    def kitchen_plug_toggle(self):
        self.plug_kueche.toggle()
