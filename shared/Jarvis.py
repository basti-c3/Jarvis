import zmq
from shared.utils import Warn


class Jarvis:
    def __init__(self):
        self._audio_queue = None
        self._stt = None
        self._tts = None
        self._plugs = {}
        self._bulbs = None

        self._stt_service_client = None
        self._tts_service_client = None

    @property
    def audio_queue(self):
        if self._audio_queue is None:
            from queue import Queue
            self._audio_queue = Queue()
        return self._audio_queue

    @property
    def stt(self):
        if self._stt is None:
            from stt.JarvisSTT import JarvisSTT
            self._stt = JarvisSTT()
        return self._stt

    @property
    def tts(self):
        if self._tts is None:
            from tts.JarvisTTS import JarvisTTS
            self._tts = JarvisTTS()
        return self._tts

    @property
    def recognizer(self):
        return self.stt.recognizer

    def plug(self, topic, is_a_light):
        if topic not in self._plugs:
            from mqtt.MqttPlug import MqttPlug
            self._plugs[topic] = MqttPlug(topic, is_a_light=is_a_light)
        return self._plugs[topic]

    @property
    def plug_lichterkette(self):
        from mqtt.mqtt_utils import PLUG_LICHTERKETTE_TOPIC
        return self.plug(PLUG_LICHTERKETTE_TOPIC, is_a_light=True)

    @property
    def plug_lampe(self):
        from mqtt.mqtt_utils import PLUG_LAMPE_TOPIC
        return self.plug(PLUG_LAMPE_TOPIC, is_a_light=True)

    @property
    def plug_fernseher(self):
        from mqtt.mqtt_utils import PLUG_FERNSEHER_TOPIC
        return self.plug(PLUG_FERNSEHER_TOPIC, is_a_light=False)

    @property
    def plug_kueche(self):
        from mqtt.mqtt_utils import PLUG_KUECHE_TOPIC
        return self.plug(PLUG_KUECHE_TOPIC, is_a_light=False)

    @property
    def bulbs(self):
        if self._bulbs is None:
            from mqtt.MqttBulb import MqttBulb
            from mqtt.mqtt_utils import BULB_1, BULB_2, BULB_3
            self._bulbs = [
                MqttBulb(BULB_1),
                MqttBulb(BULB_2),
                MqttBulb(BULB_3),
            ]
        return self._bulbs

    @property
    def stt_service_client(self):
        if self._stt_service_client is None:
            from shared.ipc import client
            self._stt_service_client = client("tcp://127.0.0.1:5555", stream_pattern=zmq.REQ)
            self._stt_service_client.setsockopt(zmq.RCVTIMEO, 3000)
        return self._stt_service_client

    @property
    def tts_service_client(self):
        if self._tts_service_client is None:
            from shared.ipc import client
            self._tts_service_client = client("tcp://127.0.0.1:5556", stream_pattern=zmq.REQ)
            self._tts_service_client.setsockopt(zmq.RCVTIMEO, 3000)
        return self._tts_service_client

    def say(self, text: str):
        try:
            self.tts_service_client.send_string(text)
            self.tts_service_client.recv()
        except zmq.error.Again:  # timeout exception
            # Log a specific error message
            Warn("ERROR in TTS: Speech to text service did not respond within timeout!")


jarvis = Jarvis()