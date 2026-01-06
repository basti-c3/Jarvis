import platform
import threading
import soundfile as sf
import sounddevice as sd
import os
import torch

from shared.Jarvis import jarvis
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

from TTS.api import TTS
from jarvis.paths import XTTS_MODEL_PATH, PRECAL_AUDIOS_PATH
from shared.utils import Warn, find_anker_usb_mic


def load_xtts_model_from_checkpoint():
    model_name = XTTS_MODEL_PATH

    # First allow some TTS classes, so that torch does not throw an error
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

    return TTS(model_name=model_name).to("cuda")


def play_audio(filename):
    filepath = str(PRECAL_AUDIOS_PATH / f"{filename}.wav")
    if platform.system() == "Windows":
        import winsound
        # Uses built-in Windows sound player
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"ERROR: No audio file in {os.path.abspath(filepath)} found to play.")
        winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
    elif platform.system() == "Linux":
        data, samplerate = sf.read(str(filepath), dtype="float32")
        sd.play(
            data,
            samplerate=samplerate,
            device=jarvis.anker_speaker_device,
            blocking=True,
        )
    else:
        raise SystemError(f"Please configure playing audio for non-configured systems before running the code. System: {platform.system()}")


def say_with_model(self, text):
    if self.processing:
        # Don't say multiple stuff at once
        return
    print("Dont wait for me,I am doing something parallelly. Processing...")
    from shared.Jarvis import jarvis

    def run():
        try:
            self.processing = True
            tts_model = jarvis.tts
            tts_model.create_and_play_audio_from_text(text)
        except Exception as e:
            Warn("Jarvis speaking error:", e)
        finally:
            self.processing = False

    threading.Thread(target=run, daemon=True).start()


def say(text: str):
    # This is a preliminary solution where Jarvis can only say already processed things. Not for future use
    match text:
        case "This is a test phrase!":
            play_audio("thisisatestphrase")
        case "I apologize, but something went wrong when trying to play something from Spotify.":
            play_audio("iapologizebutsomethingwentwrongwhentryingtoplaysomethingfromspotify")
        case "Certainly, Sir. Playing from Spotify now!":
            play_audio("certainlysirplayingfromspotifynow")
        case "Sorry Sir, but I did not find any tracks in the given playlist.":
            play_audio("sorrysirbutididnotfindanytracksinthegivenplaylist")
        case "Sorry Sir, but I did not find that playlist.":
            play_audio("sorrysirbutididnotfindthatplaylist")
        case "Sorry Sir, but I did not find that album.":
            play_audio("sorrysirbutididnotfindthatalbum")
        case "Sorry Sir, but I did not find that album by id.":
            play_audio("sorrysirbutididnotfindthatalbumbyid")
        case "Sorry Sir, but I could not find that song.":
            play_audio("sorrysirbuticouldnotfindthatsong")
        case "Sorry, but I did not find the top tracks of that artist.":
            play_audio("sorrybutididnotfindthetoptracksofthatartist")
        case "Sorry Sir, but I did not find that artist.":
            play_audio("sorrysirbutididnotfindthatartist")
        case "Sorry Sir, but I did not understand what you want me to play.":
            play_audio("sorrysirbutididnotunderstandwhatyouwantmetoplay")
        case "Sorry Sir, I did not get that, would you mind repeating that, please?":
            play_audio("sorrysirididnotgetthatwouldyoumindrepeatingthatplease")
        case "Sorry Sir, but something went terribly wrong here, please try again.":
            play_audio("sorrysirbutsomethingwentterriblywrongherepleasetryagain")
        case "Of course, Sir!":
            play_audio("ofcoursesir")
        case "Sorry, Sir. There was a problem finding the correct device where the music should be stopped.":
            play_audio("sorrysirtherewasaproblemfindingthecorrectdevicewherethemusicshouldbestopped")
        case "Most certainly, Sir! Enjoy!":
            play_audio("mostcertainlysirenjoy")
        case "Sorry, Sir. There was a problem finding the correct device where the music should be played.":
            play_audio("sorrysirtherewasaproblemfindingthecorrectdevicewherethemusicshouldbeplayed")
        case "Alright, skipping the song!":
            play_audio("alrightskippingthesong")
        case "Sorry, Sir. There was a problem finding the correct device where the music is supposed to be playing currently.":
            play_audio("sorrysirtherewasaproblemfindingthecorrectdevicewherethemusicissupposedtobeplayingcurrently")
        case "Alright, let's make an infinite loop of this song!":
            play_audio("alrightletsmakeaninfiniteloopofthissong")
        case "Turning repeat mode off again.":
            play_audio("turningrepeatmodeoffagain")
        case "Sorry, Sir. There was a problem finding the correct device where the repeat mode should be set.":
            play_audio("sorrysirtherewasaproblemfindingthecorrectdevicewheretherepeatmodeshouldbeset")
        case "Sorry, Sir. I encountered a problem executing the requested command to the Spotify API. The response was not as expected.":
            play_audio(
                "sorrysiriencounteredaproblemexecutingtherequestedcommandtothespotifyapitheresponsewasnotasexpected")
        case "Sorry, Sir. I encountered a problem executing the requested command to the MQTT devices. The response was not as expected.":
            play_audio(
                "sorrysiriencounteredaproblemexecutingtherequestedcommandtothemqttdevicestheresponsewasnotasexpected")
        case "Turning off the lights. Good night, Sir!":
            play_audio("turningoffthelightsgoodnightsir")
        case "Turning on the lights. Good morning, Sir!":
            play_audio("turningonthelightsgoodmorningsir")
        case "Enjoy a comfortable evening!":
            play_audio("enjoyacomfortableevening")
        case "Of course, here you go!":
            play_audio("ofcoursehereyougo")
        case "Sorry Sir, but the speech service is not responding.":
            play_audio("sorrysirbutthespeechserviceisnotresponding")
        case "shuttingdowngoodbyesir":
            play_audio("shuttingdowngoodbyesir")
