# import time
# import pyttsx3
# # keyword = "TourIT"
# # user = input("User: ")
# # response = "TourIT: Hi! I am TourIT, How can I help you?"

# # while True:
# #     if keyword.lower() in user.lower():
# #         print(response)
# #     else:
# #         print("None")
# wakeword = "TourIT"
# speech = pyttsx3.init()
# voices = speech.getProperty('voices')
# #speech.setProperty('voice', 'english_rp+f2')
# speech.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
# rate = speech.getProperty('rate')
# speech.setProperty('rate',150)

# while True:
#     user = input("User: ")
#     if wakeword.lower() in user.lower():
#         speech.say("I'm Listening...")
#         speech.runAndWait()
#         request = input("Request: ")
#         speech.say(request)
#         speech.runAndWait()
#     else:
#         speech.say("Wrong Input!")
#         speech.runAndWait()
from gtts import gTTS
import pymysql
import vlc

con = pymysql.connect(host="192.168.1.17", user="root", passwd="", database="tourit")
cursor = con.cursor()

query = "SELECT Script FROM script"

cursor.execute(query)
rows=cursor.fetchall()

wakeword = "TourIT"
while True:
    user = input("User: ")
    if wakeword.lower() in user.lower():
        script = str(rows[0])
        speech = gTTS(script)
        speech.save("TourIT.mp3")
        p = vlc.MediaPlayer("TourIT.mp3")
        p.play()



cursor.close()
con.close()