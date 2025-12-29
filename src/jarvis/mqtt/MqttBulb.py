from mqtt.MqttDevice import MqttDevice


class MqttBulb(MqttDevice):
    def __init__(self, client_id):
        super().__init__(client_id)

    def lights_to_normal(self):
        self.client.publish(f"cmnd/{self.topic}/Channel4", "50")
        self.client.publish(f"cmnd/{self.topic}/Channel5", "50")

