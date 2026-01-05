from jarvis.mqtt.MqttDevice import MqttDevice


class MqttPlug(MqttDevice):
    is_a_light: bool

    def __init__(self, client_id, is_a_light):
        super().__init__(client_id)
        self.is_a_light = is_a_light
