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
                play_audio("sorrysiriencounteredaproblemexecutingtherequestedcommandtothespotifyapitheresponsewasnotasexpected")

jarvis = Jarvis()
