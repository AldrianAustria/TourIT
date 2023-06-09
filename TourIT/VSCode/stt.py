import speech_recognition as sr
import vlc
from gtts import gTTS
from mutagen.mp3 import MP3
import time

status = True

while status:
    try:
        with sr.Microphone() as source:
            r = sr.Recognizer()
            print("Speak Now")
            r.adjust_for_ambient_noise(source, duration=1)
            # read the audio data from the default microphone
            # audio_data = r.record(source, duration=15)
            audio_data = r.listen(source,timeout=10,phrase_time_limit=15)
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_google(audio_data, language = 'en-us')
            speech = gTTS(text)
            speech.save("tts.mp3")
            p = vlc.MediaPlayer("tts.mp3")
            p.play()
            print(text)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.WaitTimeoutError:
        print("Hehe Goodbye!")
        status = False
    except sr.UnknownValueError:
        print("Goodbye!")
        status = False