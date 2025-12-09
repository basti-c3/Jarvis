import threading

from global_init import get_tts_model
from utils import Warn, play_audio


class Jarvis:
    processing = False

    def say_with_model(self, text):
        if self.processing:
            # Don't say multiple stuff at once
            return
        print("Dont wait for me,I am doing something parallelly. Processing...")
        def run():
            try:
                self.processing = True
                tts_model = get_tts_model()
                tts_model.create_and_play_audio_from_text(text)
            except Exception as e:
                Warn("Jarvis speaking error:", e)
            finally:
                self.processing = False

        threading.Thread(target=run, daemon=True).start()

    def say(self, text: str):
        # This is a preliminary solution where Jarvis can only say already processed things. Not for future use
        print("GOT HERE")
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


jarvis = Jarvis()
