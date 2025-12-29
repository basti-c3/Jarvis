import queue

import zmq
from vosk import KaldiRecognizer

from shared.ipc import client
from text_to_speech.JarvisTTS import JarvisTTS
from speech_to_text.JarvisSTT import JarvisSTT

_stt_model = None
_tts_model = None
_audio_queue = None

_plug_lichterkette = None
_plug_lampe = None
_plug_fernseher = None
_plug_kueche = None

_bulb_1, _bulb_2, _bulb_3 = None, None, None

stt_service = client("tcp://127.0.0.1:5555")
tts_service = client("tcp://127.0.0.1:5556")
stt_service.setsockopt(zmq.RCVTIMEO, 3000)
tts_service.setsockopt(zmq.RCVTIMEO, 3000)


def init_globals():
    global _audio_queue
    global _stt_model
    global _tts_model

    global _plug_lichterkette
    global _plug_lampe
    global _plug_fernseher
    global _plug_kueche

    if _audio_queue is None:
        _audio_queue = queue.Queue()
    if _stt_model is None:
        _stt_model = JarvisSTT()
    # if _tts_model is None:
    #    _tts_model = JarvisTTS()

    from mqtt.mqtt_utils import PLUG_LICHTERKETTE_TOPIC, PLUG_LAMPE_TOPIC, PLUG_FERNSEHER_TOPIC, PLUG_KUECHE_TOPIC
    from mqtt.MqttPlug import MqttPlug
    if _plug_lichterkette is None:
        _plug_lichterkette = MqttPlug(PLUG_LICHTERKETTE_TOPIC, is_a_light=True)
    if _plug_lampe is None:
        _plug_lampe = MqttPlug(PLUG_LAMPE_TOPIC, is_a_light=True)
    if _plug_fernseher is None:
        _plug_fernseher = MqttPlug(PLUG_FERNSEHER_TOPIC, is_a_light=False)
    if _plug_kueche is None:
        _plug_kueche = MqttPlug(PLUG_KUECHE_TOPIC, is_a_light=False)


def get_audio_queue():
    global _audio_queue
    if _audio_queue is None:
        _audio_queue = queue.Queue()
    return _audio_queue


def get_stt_model() -> JarvisSTT:
    global _stt_model
    if _stt_model is None:
        _stt_model = JarvisSTT()
    return _stt_model


def get_stt_recognizer() -> KaldiRecognizer:
    global _stt_model
    if _stt_model is None:
        _stt_model = JarvisSTT()
    return _stt_model.recognizer


def get_tts_model() -> JarvisTTS:
    global _tts_model
    if _tts_model is None:
        _tts_model = JarvisTTS()
    return _tts_model


def get_plug_lichterkette():
    from mqtt.mqtt_utils import PLUG_LICHTERKETTE_TOPIC
    from mqtt.MqttPlug import MqttPlug

    global _plug_lichterkette
    if _plug_lichterkette is None:
        _plug_lichterkette = MqttPlug(PLUG_LICHTERKETTE_TOPIC, is_a_light=True)
    return _plug_lichterkette


def get_plug_lampe():
    from mqtt.MqttPlug import MqttPlug
    from mqtt.mqtt_utils import PLUG_LAMPE_TOPIC

    global _plug_lampe
    if _plug_lampe is None:
        _plug_lampe = MqttPlug(PLUG_LAMPE_TOPIC, is_a_light=True)
    return _plug_lampe


def get_plug_fernseher():
    from mqtt.MqttPlug import MqttPlug
    from mqtt.mqtt_utils import PLUG_FERNSEHER_TOPIC

    global _plug_fernseher
    if _plug_fernseher is None:
        _plug_fernseher = MqttPlug(PLUG_FERNSEHER_TOPIC, is_a_light=False)
    return _plug_fernseher


def get_plug_kueche():
    from mqtt.MqttPlug import MqttPlug
    from mqtt.mqtt_utils import PLUG_KUECHE_TOPIC

    global _plug_kueche
    if _plug_kueche is None:
        _plug_kueche = MqttPlug(PLUG_KUECHE_TOPIC, is_a_light=False)
    return _plug_kueche


def get_light_bulbs() -> []:
    from mqtt.MqttBulb import MqttBulb
    from mqtt.mqtt_utils import BULB_1, BULB_2, BULB_3

    global _bulb_1, _bulb_2, _bulb_3
    if _bulb_1 is None:
        _bulb_1 = MqttBulb(BULB_1)
        _bulb_2 = MqttBulb(BULB_2)
        _bulb_3 = MqttBulb(BULB_3)
    return [_bulb_1, _bulb_2, _bulb_3]