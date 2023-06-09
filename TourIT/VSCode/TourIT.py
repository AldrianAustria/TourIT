from gtts import gTTS
from mutagen.mp3 import MP3
import openai
import time
import pymysql
import serial
import vlc
import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk
import threading

Arduino = serial.Serial('/dev/ttyUSB0', 9600)

query_word = "The tour for this exhibit is now done, I am now open for questions. Be reminded that if there are no response within 15 seconds, i will be continuing the tour."
cont_word = "If there are no anymore questions, i will be now continuing the tour, please be reminded that keep my path unobstracted."
last_word = "Thank you"

wakeword = "Martha"
byte = '1'
byte_block = '0'
station_start = False
arduino_value = -1

delay_respond = None
respond = True
command_send = False
block_send = False
end_tour = False
receive = False

openai.api_key = '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'
messages = [ {"role": "system", "content": 
              'You are Martha, an artificial intelligence that can tour and answer questions of visitors and you are currently at Father George J. Willmann, SJ Museum. Answer the questions short and be concise. Remember the following statements are true and you can use it as reference: George J. Willmann was born in Brooklyn, New York on June 29, 1897. His parents were William Godfrey Willmann and Julia Corcoran Willmann. George had two brothers, Edward and William Jr., and four sisters, Miriam, Dorothy, Ruth and Agnes. His sisters Ruth and Agnes became members of Franciscan Missionaries of Mary in their later lives. From 1902 to 1908, Willmann studied at the Our Lady of Good Counsel Grammar School in Brooklyn, from 1908 to 1913 and at the Boys High and Brooklyn Preparatory School. On August 15, 1915, Willmann entered the into Society of Jesus Seminary at Poughkeepsie, New York. He completed his Novitiate and Juniorate by 1922. Willmann came to the Philippines in 1922 as a seminarian to accomplish a teaching stint at the Ateneo de Manila and later returned to the United States in 1925 to continue his theological studies.'
              +'On June 20, 1928, Willmann was ordained at the Woodstock College in Maryland by Archbishop Michael Joseph Curley. Willmann took Tertianship in Poughkeepsie. Willmann served as Director of New York Jesuit Seminary and Mission Bureau from 1930 to 1936. Willmann returned to the Philippines in November 1936 continue teaching at the Ateneo de Manila. He also served as Prefect of Discipline & Treasurer at the same education institution from 1936 to 1937. In 1937 he served as the Session Director of the First National Eucharistic Congress in Manila and on the same year became dean of Ateneo de Manila. In 1938, Willmann established the Catholic Youth Organization in the Philippines, a religious and recreational organization for the youth. He became the chaplain of the organization on its establishment until 1977. Willmann was also initiated into Order of Knights of Columbus June 30 of the same year. He was appointed Chaplain of Manila Council 1000 based in Intramuros, Manila, with Jose Galan y Blanco, his long-time associate at the Ateneo de Manila, as his proposer. Servicemen clubs were established under the guidance of the Army-Navy Morale Committee, which Willmann and the auxiliary bishop of Manila, Rufino Santos, were members of in December 1941. In 1942, Willmann entered the Manila San Jose Seminary as a teacher in Social Sciences. He became treasurer of the seminary in 1948. He taught at the seminary until 1951. Willmann became a prisoner of war during the Japanese occupation of Manila where he was arrested at the University of Santo Tomas by the Japanese in July 1944. He and the other prisoners where later put into a concentration camp in Los Banos, Laguna and was later freed by American forces in 1945. On July 1, 1975, Willmann was granted Filipino citizenship by then President Ferdinand Marcos through Presidential Decree No. 740 for his "virtuous acts, compassionate and kind and loving service for the Filipino people,". On June 29, 1977, Pope Paul VI awarded Willmann the Pro Ecclesia et Pontifice medal, the highest award the Pope can give to a laity.'
              +'Willmann went to United States in August 1977 for the 95th Annual Supreme Council Convention which took place from August 14 to 17 at Indianapolis in Indiana. Willmann led the Philippine delegation with Bro. Nicanor Y. Fuentes and Bro Concelio B. Cagurangan.Willmann later went to New York presumely to pay a visit to his sisters, Ruth, and Agnes Franciscan nun living in Roslyn, and his nephew James and niece Mary Ruth. The priest was prone to falls because of his weak limbs and had a fall while he was in New York, and needed a hip-bone surgery. The priest was initially confined at St. Francis Hospital in Roslyn. He was later transferred to Murray-Weigel Hall, a Jesuit infirmary at Fordham University in Fordham, the Bronx, New York City on September 8, 1977. Willmann was later discharged and stayed at the Jesuit House at Fordham. Willmann, died on September 14, 1977, due to cardiac arrest. Willmann\'s remains were interred at the Jesuit Cemetery in Novaliches, Quezon City, Philippines.'
              +'The Knights of Columbus established its presence in the Philippines in early 1905, but Willmann was credited for cementing the organization\'s presence after he took leadership of the group after the World War II. The priest continuously resided in the Philippines since 1936. He also helped established the presence of various organization in the country such as the Daughters of Mary Immaculate (DMI) which was established as the Daughters of Isabella in 1951, Knights of Columbus Fraternal Association in the Philippines, Inc (KCFAPI), KC Foundations, Columbian Squires, and the Catholic Youth Organization (CYO). The National Executive Committee, led by former Chief Justice Hilario Davide, Jr. and Pedro C. Quitorio as Vice-Chairman, was created to campaign for Willmann\'s beatification which may lead to the priest\'s sainthood.'
              +'One of the few but timely and efficacious blessings with the Order in the Philippines experienced during the lean years of 1930\'s, came in the person of an American Jesuit priest, Fr. George J. Willmann.  Born on June 29, 1897, in Brooklyn, New York, he first came to the Philippines in 1922 when he was still a seminarian, to fulfill a teaching stint at the Ateneo de Manila. Then after completing his studies and being ordained in the United States, he was sent back to Manila and all of his priestly life had been spent there. A remark by one his contemporary fellow Jesuit reflected the impact which Fr. Willmann made on the Knights of Columbus in the Philippines during the latter half of the 1930\'s. Father Willmann was like a glimmer of light in an otherwise dark decade. He has the following recollection about his first awareness of the Knights of Columbus.'
              +'Father Willmann\'s early association with the Knights of Columbus in the Philippines may also be established through his participation in the Youth Program that was launched by Manila Council 1000 in the early 30\'s.  His article, entitled "The Knights Stayed on the Job," constitutes the only surviving firsthand account of the development and implementation of the program. The use of the Ateneo basketball court in Ermita which belonged to Fr. Willmann\'s religious Order as one of the first venues for the program\'s basketball leagues, also points to his direct involvement in the Columbian activity.  His concern for the underprivileged youth, according to an observation by a fellow Jesuit, motivated Father Willmann to join the Knights of Columbus in 1938.'
              +'In August 1977, Father Willmann went to the United States for the Ninety-Fifth Annual Supreme Council Convention in Indianapolis, Indiana, as the head of the Philippine delegation. After the convention, he visited his sister in New York but suffered a fall that required a hip-bone surgery. He was initially confined to St. Francis Hospital in Roslyn and later transferred to Murray-Weigel Hall in New York Province. He was discharged from the hospital to recuperate at the Jesuit House at Fordham, but on September 14, 1977, he passed away due to a cardiac arrest, much to the distress of those who had hoped for his recovery.'
              +'The First Knights of Columbus National Convention in the Philippines was held from November 29 to December 2, 1949, during Father Willmann\'s term as Philippine District Deputy. The Convention focused on the urgency of the threats of Communism in the country, as expressed by Most Reverend Alejando Olalia, D.D., Coadjutor Bishop of Tuguegarao, Cagayan, in his “Message”. The Convention was significant as it united the efforts and minds of the Knights in preserving and furthering the Christian civilization heritage.'
              +'Notable among his many accomplishments are the establishment of Catholic Youth Organization in the Philippines (1938), Catholics Press that published \"Filipinas\" and \"Cross\" Magazines (1946), Columbian Squires in the Philippines (1950), Daughters of Isabella in the Philippines (1951) which was later reorganized under the name Daughters of Mary Immaculate (DMI), Columbian Farmers Aid Association (1951), later reorganized under the name of Knights of Columbus Community Service, Inc. (1962), Knights of Columbus Fraternal Association of the Philippines, Inc. (1958), and Knights of Columbus Philippines Foundation, Inc. (1971).'
              +'Father George J. Willmann, an American Jesuit Priest, is known as the "Father McGivney of the Philippines" and "Father of Knights of Columbus in the Philippines" because of his role in propagating the Knights of Columbus in the country. He expanded the Order throughout the country, especially among the poor, and established various organizations, including the Knights of Columbus Fraternal Association of the Philippines, Inc. and Knights of Columbus Community Service, Inc. He also established community-based cooperative credit unions in many dioceses throughout the country, which numbered 135 by 1964. Fr. Willmann\'s work with the press was noteworthy, and he received recognition for his service to the Church, academia, and society. He died in 1977 at the age of 80 but continued to inspire and guide the growth of the Knights of Columbus in the Philippines even after his death. Fr. Willmann was an embodiment of the Knights of Columbus\' theme "Faith in Action," and his work focused on improving the social and economic conditions of both rural and urban communities.'
              +'The Knights of Columbus have been promoting the sanctity of Father Willmann, with membership to the Fr. Willmann Fellows open to all since 2001. As of December 31, 2021, 1,208 individuals and 32 institutions nationwide have joined this fellowship. In 2015, the Diocesan Phase of the Cause of the Servant of God, Fr. George J. Willmann was opened, and a Tribunal was convened to hear about 50 witnesses. However, the Cause was halted from 2017 to 2019 due to the transfer of competence from the Archdiocese of New York to Manila. In 2019, the transfer of competence was granted by Timothy Cardinal Dolan, and in January 2021, the "Nihil Obstat" was granted by the Congregation for the Causes of Saints. On July 4, 2022, the new Archbishop of Manila caused the resumption of the Diocesan Phase of the Cause of Fr. George J. Willmann.'
              +'The Fr. George J. Willmann, SJ Museum was blessed and inaugurated on July 5, 2013. It is located at the 2nd floor of the Fr. George J. Willmann, SJ Memorial Building in Intramuros, Manila, which was also inaugurated and blessed on the same ceremony. The blessing was presided by then Manila Archbishop Luis Antonio Cardinal Tagle together with Cebu Archbishop Jose Palma who was then the President of the Catholic Bishops\' Conference of the Philippines. The Museum was designed by Fr. Alex Bautista together with Msgr. Pedro Quitorio who supplied storyline and the texts. While it displays a rare collection of personal artifacts of Fr. George J Willmann, it also tells in murals about his life and fruitful ministry. The Museum is open at 8AM till 5PM frpm Monday to Friday and it is located at Cabildo cor. Sta. Potenciana St. Intramuros, Manila, Intramuros, Manila, 1002 Metro Manila, Philippines.'
              +'Father Willmann was appointed as the first district deputy in the Philippines in 1948, on March 1, 1954, he became the territorial deputy, and in 1962, he became the Philippine deputy, a position held until his death. He was buried at Novaliches in the Philippines. Manila Council 1000 is the first council in the Philippines established on April 23, 1905'}]

class GIFPlayer:
    def __init__(self, root, gif_path):
        self.root = root
        self.gif_path = gif_path
        self.gif = None
        self.canvas = None
        self.photo = None
        
    def play(self, duration):
        self.gif = Image.open(self.gif_path)
        width, height = self.gif.size
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack(padx=x, pady=y)
        self.show_frame()

        self.root.after(duration, self.close)

    def show_frame(self):
        try:
            self.gif.seek(self.gif.tell()+1)
        except EOFError:
            self.gif.seek(0)

        self.photo = ImageTk.PhotoImage(self.gif)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.root.after(50, self.show_frame)

    def close(self):
        self.root.destroy()

def run_gif_player(gif_path, duration):
    root = tk.Tk()
    #root.attributes('-topmost', True)
    root.attributes('-fullscreen', True)
    root.geometry('{}x{}+0+0'.format(root.winfo_screenwidth(), root.winfo_screenheight())) # Set geometry of root window
    player = GIFPlayer(root, gif_path)
    player.play(duration)
    root.mainloop()

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

def speech_input(station_status):
    status = True
    while status:
        message = ""
        try:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                print("Speak Now")
                r.adjust_for_ambient_noise(source, duration=1)
                # read the audio data from the default microphone
                # audio_data = r.record(source, duration=15)
                audio_data = r.listen(source,timeout=15,phrase_time_limit=20)
                print("Recognizing...")
                # convert speech to text
                message = r.recognize_google(audio_data)
                print(message)
                if station_status:
                    messages.append(
                    {"role": "user", "content": message}
                    )
                    chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=messages
                    )
                    reply = (chat.choices[0].message.content).lower().replace(', ',',').replace('j. ','j ').replace('no. ','number ').replace('fr. ','father')
                    delay_respond = script_to_mp3("reply.mp3", reply)
                    thread = threading.Thread(target=run_gif_player, args=('gifs/listen.gif', int(delay_respond*1000)))
                    thread.start()
                    thread.join()
                    messages.append({"role": "assistant", "content": reply})
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.WaitTimeoutError:
            print("Timed Out!")
            status = False
        except sr.UnknownValueError:
            print("No Input Detected")
            status = False
        return message, status

while True:
    if(arduino_value == 0 and station_start == False):
        con = pymysql.connect(host="192.168.0.101", user="root", passwd="", database="tourit")
        cursor = con.cursor()
        query = "SELECT Script FROM script"
        cursor.execute(query)
        rows = cursor.fetchall()
        end_tour = False
        receive = False
        while receive == False:
            userInput, receive = speech_input(station_start)
        if wakeword.lower() in userInput.lower():
            command_send = True
            station_start = True
            print("Station 0 Start")
            sleep_time = script_to_mp3("mp3_files/Intro.mp3", rows[0])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            print("Station 0 Done")
        else:
            Arduino.write(byte_block.encode())
            receive = False
            station_start = False
            sleep_time = script_to_mp3("mp3_files/Intro_fail.mp3", rows[11])
            thread = threading.Thread(target=run_gif_player, args=('gifs/SAD.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            print("Didn't understand")

    if(Arduino.inWaiting() > 0):
        arduino_value = int(Arduino.readline().decode().strip())
        # if(arduino_value != 100):
        #     con1 = pymysql.connect(host="192.168.132.174", user="root", passwd="", database="tourit")
        #     cursor1 = con1.cursor()

        #     query1 = "UPDATE location SET `loc`=%s WHERE `id`=1"

        #     cursor1.execute(query1, (arduino_value,))
        #     con1.commit()

        #     cursor1.close()
        #     con1.close()
        
        
        ##############################
        if(arduino_value == 1):
            command_send = True
            print("Station 1 Start")
            sleep_time = script_to_mp3("mp3_files/Script1.mp3", rows[1])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 1 Done")

        if(arduino_value == 2):
            command_send = True
            print("Station 2 Start")
            sleep_time = script_to_mp3("mp3_files/Script2.mp3", rows[2])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 2 Done")

        if(arduino_value == 3):
            command_send = True
            print("Station 3 Start")
            sleep_time = script_to_mp3("mp3_files/Script3.mp3", rows[3])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 3 Done")
        
        if(arduino_value == 4):
            command_send = True
            print("Station 4 Start")
            sleep_time = script_to_mp3("mp3_files/Script4.mp3", rows[4])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 4 Done")
        
        if(arduino_value == 5):
            command_send = True
            print("Station 5 Start")
            sleep_time = script_to_mp3("mp3_files/Script5.mp3", rows[5])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 5 Done")
        
        if(arduino_value == 6):
            command_send = True
            print("Station 6 Start")
            sleep_time = script_to_mp3("mp3_files/Script6.mp3", rows[6])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 6 Done")
        
        if(arduino_value == 7):
            command_send = True
            print("Station 7 Start")
            sleep_time = script_to_mp3("mp3_files/Script7.mp3", rows[7])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 7 Done")
        
        if(arduino_value == 8):
            command_send = True
            print("Station 8 Start")
            sleep_time = script_to_mp3("mp3_files/Script8.mp3", rows[8])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 8 Done")
        
        if(arduino_value == 9):
            command_send = True
            print("Station 9 Start")
            sleep_time = script_to_mp3("mp3_files/Script9.mp3", rows[9])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", cont_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 9 Done")

        if(arduino_value == 10):
            command_send = True
            print("Station 10 Start")
            sleep_time = script_to_mp3("mp3_files/Script10.mp3", rows[10])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            sleep_time = script_to_mp3("mp3_files/queries.mp3", query_word)
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            while respond == True:
                ret, respond = speech_input(station_start)
            sleep_time = script_to_mp3("mp3_files/continue.mp3", rows[14])
            thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', int(sleep_time*1000)))
            thread.start()
            thread.join()
            respond = True
            print("Station 10 Done")
            station_start = False
            end_tour = True

        if(arduino_value == 100):
            if(station_start == False and end_tour == False):
                arduino_value = 0
                receive = False
                block_send = False
                command_send = False
                Arduino.write(byte_block.encode())
            else:
                block_send = True
                print("Excuse Start")
                sleep_time = script_to_mp3("mp3_files/Excuse.mp3", rows[12])
                thread = threading.Thread(target=run_gif_player, args=('gifs/SAD.gif', int(sleep_time*1000)))
                thread.start()
                thread.join()
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
            receive = False
            block_send = False
            command_send = False
            Arduino.write(byte_block.encode())

    if(command_send == True):
        Arduino.write(byte.encode())
        command_send = False


cursor.close()
con.close()