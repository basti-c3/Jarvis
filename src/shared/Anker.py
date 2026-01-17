from shared.utils import find_anker_usb_mic, find_anker_usb_speaker


class Anker:
    def __init__(self):
        self._anker_mic_device = None
        self._audio_mic_sample_rate = None
        self._audio_speaker_sample_rate = None
        self._anker_speaker_device = None

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


anker = Anker()
