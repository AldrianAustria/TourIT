import vlc
from gtts import gTTS
from mutagen.mp3 import MP3
import time

speech = gTTS("I cant understand you, please try again.")
speech.save("Intro_fail2.mp3")
file = "Intro_fail2.mp3"
p = vlc.MediaPlayer(file)
p.play()
audio = MP3(file)
time.sleep(audio.info.length)
print("Didn't understand")