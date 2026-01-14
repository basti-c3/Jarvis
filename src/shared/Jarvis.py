import zmq

from jarvis.core.services import send_tts_service
from shared.utils import Warn, find_anker_usb_mic, find_anker_usb_speaker


class Jarvis:
    def __init__(self):
        self._wake_word = None
        self._audio_queue = None

        self._stt = None
        self._tts = None

        self._plugs = {}
        self._bulbs = None

        self._anker_mic_device = None
        self._audio_mic_sample_rate = None
        self._audio_speaker_sample_rate = None
        self._anker_speaker_device = None

    @property
    def audio_queue(self):
        if self._audio_queue is None:
            from queue import Queue
            self._audio_queue = Queue()
        return self._audio_queue

    @property
    def wake_word(self):
        if self._wake_word is None:
            from jarvis.core.WakeWordEngine import WakeWordEngine
            self._wake_word = WakeWordEngine()
        return self._wake_word

    @property
    def tts(self):
        if self._tts is None:
            from tts_service.JarvisTTS import JarvisTTS
            self._tts = JarvisTTS()
        return self._tts

    @property
    def recognizer(self):
        return self.stt.recognizer

    def plug(self, topic, is_a_light):
        if topic not in self._plugs:
            from jarvis.mqtt.MqttPlug import MqttPlug
            self._plugs[topic] = MqttPlug(topic, is_a_light=is_a_light)
        return self._plugs[topic]

    @property
    def plug_lichterkette(self):
        from jarvis.mqtt.mqtt_utils import PLUG_LICHTERKETTE_TOPIC
        return self.plug(PLUG_LICHTERKETTE_TOPIC, is_a_light=True)

    @property
    def plug_lampe(self):
        from jarvis.mqtt.mqtt_utils import PLUG_LAMPE_TOPIC
        return self.plug(PLUG_LAMPE_TOPIC, is_a_light=True)

    @property
    def plug_fernseher(self):
        from jarvis.mqtt.mqtt_utils import PLUG_FERNSEHER_TOPIC
        return self.plug(PLUG_FERNSEHER_TOPIC, is_a_light=False)

    @property
    def plug_kueche(self):
        from jarvis.mqtt.mqtt_utils import PLUG_KUECHE_TOPIC
        return self.plug(PLUG_KUECHE_TOPIC, is_a_light=False)

    @property
    def bulbs(self):
        if self._bulbs is None:
            from jarvis.mqtt.MqttBulb import MqttBulb
            from jarvis.mqtt.mqtt_utils import BULB_1, BULB_2, BULB_3
            self._bulbs = [
                MqttBulb(BULB_1),
                MqttBulb(BULB_2),
                MqttBulb(BULB_3),
            ]
        return self._bulbs

    @property
    def audio_mic_sample_rate(self):
        if self._audio_mic_sample_rate is None:
            device_index, samplerate = find_anker_usb_mic()
            if samplerate >= 44000 and samplerate <= 48000:  # fix this range to 48000 to get less errors
                self._audio_mic_sample_rate = 48000
            else:
                self._audio_mic_sample_rate = samplerate
            self._anker_mic_device = device_index
        return self._audio_mic_sample_rate

    @property
    def anker_mic_device(self):
        if self._anker_mic_device is None:
            device_index, samplerate = find_anker_usb_mic()
            self._audio_mic_sample_rate = samplerate
            self._anker_mic_device = device_index
        return self._anker_mic_device

    @property
    def anker_speaker_device(self):
        if self._anker_speaker_device is None:
            device_index, samplerate = find_anker_usb_speaker()
            self._audio_speaker_sample_rate = samplerate
            self._anker_speaker_device = device_index
        return self._anker_speaker_device

    @property
    def audio_speaker_sample_rate(self):
        if self._audio_speaker_sample_rate is None:
            device_index, samplerate = find_anker_usb_speaker()
            self._audio_speaker_sample_rate = samplerate
            self._anker_speaker_device = device_index
        return self._audio_speaker_sample_rate

    def say(self, text: str):
        try:
            send_tts_service(text)
        except zmq.error.Again:  # timeout exception
            # Log a specific error message
            Warn("ERROR in TTS: Speech to text service did not respond within timeout!")


jarvis = Jarvis()
