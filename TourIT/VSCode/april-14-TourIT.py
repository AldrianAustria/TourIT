from gtts import gTTS
from mutagen.mp3 import MP3
import time
import pymysql
import serial
import vlc
import speech_recognition as sr

Arduino = serial.Serial('/dev/ttyUSB0', 9600)

wakeword1 = "Martha"
wakeword2 = "Marta"
byte = '1'
byte_block = '0'
station_start = False
arduino_value = -1

command_send = False
block_send = False
end_tour = False
recieve = False

def script_to_mp3(file_name, db_script):
    script = str(db_script)
    speech = gTTS(script)
    speech.save(file_name)
    p = vlc.MediaPlayer()
    media = vlc.Media(file_name)
    p.set_media(media)
    p.play()
    audio = MP3(file_name)
    return audio.info.length

def speech_input():
    status = True
    while status:
        text = ""
        try:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                print("Speak Now")
                r.adjust_for_ambient_noise(source, duration=1)
                # read the audio data from the default microphone
                # audio_data = r.record(source, duration=15)
                audio_data = r.listen(source,timeout=5,phrase_time_limit=15)
                print("Recognizing...")
                # convert speech to text
                text = r.recognize_google(audio_data, language = 'en-US')
                print(text)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.WaitTimeoutError:
            print("Timed Out!")
            status = False
        except sr.UnknownValueError:
            print("No Input Detected")
            status = False
        return text, status

while True:
    if(arduino_value == 0 and station_start == False):
        con = pymysql.connect(host="192.168.1.17", user="root", passwd="", database="tourit")
        cursor = con.cursor()
        query = "SELECT Script FROM script"
        cursor.execute(query)
        rows = cursor.fetchall()
        end_tour = False
        recieve = False
        while recieve == False:
            userInput, recieve = speech_input()
        if wakeword1.lower() or wakeword2.lower() in userInput.lower():
            command_send = True
            station_start = True
            print("Station 0 Start")
            sleep_time = script_to_mp3("mp3_files/Intro.mp3", rows[0])
            time.sleep(sleep_time)
            print("Station 0 Done")
        else:
            Arduino.write(byte_block.encode())
            recieve = False
            station_start = False
            sleep_time = script_to_mp3("mp3_files/Intro_fail.mp3", rows[11])
            time.sleep(sleep_time)
            print("Didn't understand")

    if(Arduino.inWaiting() > 0):
        arduino_value = int(Arduino.readline().decode().strip())
        if(arduino_value == 1):
            command_send = True
            print("Station 1 Start")
            sleep_time = script_to_mp3("mp3_files/Script1.mp3", rows[1])
            time.sleep(sleep_time)
            print("Station 1 Done")

        if(arduino_value == 2):
            command_send = True
            print("Station 2 Start")
            sleep_time = script_to_mp3("mp3_files/Script2.mp3", rows[2])
            time.sleep(sleep_time)
            print("Station 2 Done")

        if(arduino_value == 3):
            command_send = True
            print("Station 3 Start")
            sleep_time = script_to_mp3("mp3_files/Script3.mp3", rows[3])
            time.sleep(sleep_time)
            print("Station 3 Done")
        
        if(arduino_value == 4):
            command_send = True
            print("Station 4 Start")
            sleep_time = script_to_mp3("mp3_files/Script4.mp3", rows[4])
            time.sleep(sleep_time)
            print("Station 4 Done")
        
        if(arduino_value == 5):
            command_send = True
            print("Station 5 Start")
            sleep_time = script_to_mp3("mp3_files/Script5.mp3", rows[5])
            time.sleep(sleep_time)
            print("Station 5 Done")
        
        if(arduino_value == 6):
            command_send = True
            print("Station 6 Start")
            sleep_time = script_to_mp3("mp3_files/Script6.mp3", rows[6])
            time.sleep(sleep_time)
            print("Station 6 Done")
        
        if(arduino_value == 7):
            command_send = True
            print("Station 7 Start")
            sleep_time = script_to_mp3("mp3_files/Script7.mp3", rows[7])
            time.sleep(sleep_time)
            print("Station 7 Done")
        
        if(arduino_value == 8):
            command_send = True
            print("Station 8 Start")
            sleep_time = script_to_mp3("mp3_files/Script8.mp3", rows[8])
            time.sleep(sleep_time)
            print("Station 8 Done")
        
        if(arduino_value == 9):
            command_send = True
            print("Station 9 Start")
            sleep_time = script_to_mp3("mp3_files/Script9.mp3", rows[9])
            time.sleep(sleep_time)
            print("Station 9 Done")

        if(arduino_value == 10):
            command_send = True
            print("Station 10 Start")
            sleep_time = script_to_mp3("mp3_files/Script10.mp3", rows[10])
            time.sleep(sleep_time)
            print("Station 10 Done")
            station_start = False
            end_tour = True

        if(arduino_value == 100):
            if(station_start == False and end_tour == False):
                arduino_value = 0
                recieve = False
                block_send = False
                command_send = False
                Arduino.write(byte_block.encode())
            else:
                block_send = True
                print("Excuse Start")
                sleep_time = script_to_mp3("mp3_files/Excuse.mp3", rows[12])
                time.sleep(sleep_time)
                print("Excuse Done")

        if(block_send == True):
            Arduino.write(byte_block.encode())
            Arduino.write(byte.encode())
            block_send = False

        if(command_send == True):
            Arduino.write(byte.encode())
            command_send = False

        if(station_start == False and end_tour == False):
            arduino_value = 0
            recieve = False
            block_send = False
            command_send = False
            Arduino.write(byte_block.encode())

    if(command_send == True):
        Arduino.write(byte.encode())
        command_send = False


cursor.close()
con.close()