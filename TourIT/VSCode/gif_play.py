import tkinter as tk
from PIL import Image, ImageTk
import time
import threading

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

def run_gif_player(gif_path, duration=5000):
    root = tk.Tk()
    #root.attributes('-topmost', True)
    root.attributes('-fullscreen', True)
    root.geometry('{}x{}+0+0'.format(root.winfo_screenwidth(), root.winfo_screenheight())) # Set geometry of root window
    player = GIFPlayer(root, gif_path)
    player.play(duration)
    root.mainloop()

thread = threading.Thread(target=run_gif_player, args=('gifs/standby.gif', 5000))
thread.start()
thread.join()
thread = threading.Thread(target=run_gif_player, args=('gifs/SAD.gif', 5000))
thread.start()
thread.join()
thread = threading.Thread(target=run_gif_player, args=('gifs/listen.gif', 5000))
thread.start()
thread.join()
thread = threading.Thread(target=run_gif_player, args=('gifs/talking.gif', 5000))
thread.start()
thread.join()

while True:
    print ("Hello World")