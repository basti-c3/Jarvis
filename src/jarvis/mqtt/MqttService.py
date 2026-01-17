from jarvis.mqtt.MqttBulb import MqttBulb
from jarvis.mqtt.MqttPlug import MqttPlug
from jarvis.mqtt.mqtt_utils import *
from jarvis.mqtt.mqtt_action import mqtt_action


class MqttService:
    def __init__(self):
        self.plug_lichterkette = MqttPlug(PLUG_LICHTERKETTE_TOPIC, is_a_light=True)
        self.plug_lampe = MqttPlug(PLUG_LAMPE_TOPIC, is_a_light=True)
        self.plug_fernseher = MqttPlug(PLUG_FERNSEHER_TOPIC, is_a_light=False)
        self.plug_kueche = MqttPlug(PLUG_KUECHE_TOPIC, is_a_light=False)

        self.all_plugs = [self.plug_lichterkette, self.plug_lampe, self.plug_fernseher, self.plug_kueche]
        self.all_bulbs = [MqttBulb(t) for t in (BULB_1, BULB_2, BULB_3)]

    @mqtt_action("Turning off the lights. Good night, Sir!")
    def turn_off_lights(self):
        for plug in self.all_plugs:
            if plug.is_a_light:
                plug.turn_off()
        for bulb in self.all_bulbs:
            bulb.turn_off()

    @mqtt_action("Turning on the lights. Good morning, Sir!")
    def turn_on_lights(self):
        for plug in self.all_plugs:
            if plug.is_a_light:
                plug.turn_off()
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
        self.plug_lampe.turn_on()

    @mqtt_action("Of course, here you go!")
    def turn_kitchen_plug_on(self):
        self.plug_kueche.turn_on()

    @mqtt_action("Of course, here you go!")
    def turn_kitchen_plug_off(self):
        self.plug_kueche.turn_off()

    @mqtt_action("Of course, here you go!")
    def kitchen_plug_toggle(self):
        self.plug_kueche.toggle()


mqtt_service = MqttService()
