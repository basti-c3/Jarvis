from mqtt.MqttDevice import MqttDevice


class MqttBulb(MqttDevice):
    def __init__(self, client_id):
        super().__init__(client_id)
