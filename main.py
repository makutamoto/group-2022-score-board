import enum
import tkinter as tk
import tkinter.font as tkFont
import json
import pygame
import serial
import sys

import receipt

PLAYING = './playing.ogg'
SHOOT = './shoot.ogg'
TITLE = './title.ogg'

app = tk.Tk()

ser = None

class Seg(tk.Canvas):
    font_name = "DSEG14 Classic"
    on = True
    def __init__(self, parent, height, value, color, background, digit):
        self.font = (self.font_name, height)
        self.digit = digit
        self.color = color
        self.background = background
        self.pad = height * 0.1
        info = tkFont.Font(family=self.font_name, size=height)
        width = digit * info.measure("m")
        linespace = info.metrics()['linespace']
        tk.Canvas.__init__(self, parent, width=width + self.pad * 2, height=linespace + 2 * self.pad, background="black")

        self.set_value(value)
        self.draw_value()
            
    def set_value(self, value):
        self.value = value
        self.draw_value()

    def draw_value(self):
        self.delete("all")
        value_str = str(self.value)
        self.create_text(self.pad, self.pad, text="".join(['~' for _ in range(self.digit)]), fill=self.background, font=self.font, anchor=tk.NW)
        if self.on:
            self.create_text(self.pad, self.pad, text="".join(['!' for _ in range(self.digit - len(value_str))]) + value_str, fill=self.color, font=self.font, anchor=tk.NW)

    def set_on(self, value):
        self.on = value
        self.draw_value()

class SegWithTitle(tk.Frame):
    def __init__(self, parent, title, value, height=100, color="red", background="#520000", digit=3):
        tk.Frame.__init__(self, parent)
        self.seg = Seg(self, height, value, color, background, digit)
        self.seg.grid(column=0, row=0)
        titleFont = tkFont.Font(family="PixelMplus12", size=int(height * 0.3))
        title = tk.Label(self, text=title, font=titleFont)
        title.grid(column=0, row=1)

    def set_value(self, value):
        self.seg.set_value(value)
    
    def set_on(self, value):
        self.seg.set_on(value)

class Scene(enum.Enum):
    NONE = enum.auto()
    TITLE = enum.auto()
    GAME = enum.auto()


class ScoreBoard(tk.Frame):
    titleFont = tkFont.Font(family="PixelMplus12", size=100)
    segFont = tkFont.Font(family="DSEG7 Classic Bold Italic", size=32)
    
    mode = Scene.NONE

    DATA = './data.json'
    TIME =  60

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.data = self.load_data()

        self.titleFrame = tk.Frame(self)
        self.titleFrame.grid(row=0, column=0, sticky="new")

        self.titleLabel = tk.Label(self.titleFrame, text="SHOOTING GAME", font=self.titleFont)
        self.titleLabel.grid(column=1, row=0)

        self.scoreSeg = SegWithTitle(self, "SCORE", 0, height=200)
        self.scoreSeg.grid(column=0, row=4)
        
        self.subFrame = tk.Frame(self)
        self.subFrame.grid(column=0, row=5)
        self.subFrame.grid_columnconfigure(0, weight=1)
        self.subFrame.grid_columnconfigure(3, weight=1)

        self.recordSeg = SegWithTitle(self.subFrame, "RECORD", self.data['record'], height=100, color="#00ff1e", background="#003606")
        self.recordSeg.grid(column=0, row=0, sticky=tk.NE)
        
        self.timeSeg = SegWithTitle(self.subFrame, "TIME", self.TIME, height=100, color="#ffe100", background="#2e2900")
        self.reset_time()
        self.timeSeg.grid(column=2, row=0, sticky=tk.NE)

        self.playingSound = pygame.mixer.Sound(PLAYING)
        self.playingSound.set_volume(0.5)
        self.shootSound = pygame.mixer.Sound(SHOOT)
        self.titleSound = pygame.mixer.Sound(TITLE)

        self.title()
        if ser != None:
            self.communication()

    index = 0
    title_text = '!!!PRES!BTN!!'
    def title(self):
        if self.mode == Scene.TITLE:
            return
        self.index = 0
        self.mode = Scene.TITLE
        self.titleAnimation()
        self.reset_time()
        self.play_bgm(self.titleSound)
    
    def titleAnimation(self):
        if self.mode != Scene.TITLE:
            return
        if self.index == len(self.title_text) - 1:
            self.index = 0
        self.scoreSeg.set_value(self.title_text[self.index:self.index + 3])
        self.index += 1
        app.after(300, self.titleAnimation)
    
    def load_data(self):
        data = { "record": 0 }
        try:
            with open(self.DATA, 'r') as f:
                data = json.load(f)
        except:
            pass
        return data

    def record(self):
        if self.data['record'] < self.score:
            with open(self.DATA, 'w') as f:
                json.dump({ 'record': self.score }, f)
            self.load_data()
            self.recordSeg.set_value(self.score)
            self.show_record()

    def show_record(self):
        self.recordSeg.set_on(self.blink % 2 == 0)
        if self.blink == 6:
            self.blink = 0
            return
        self.blink += 1
        app.after(250, self.show_record)
    
    def reset_time(self):
        self.time = self.TIME
        self.timeSeg.set_value(self.time)

    def start(self):
        if self.mode == Scene.GAME:
            return
        self.mode = Scene.GAME
        self.scoreSeg.set_value(0)
        self.score = 0
        self.reset_time()
        self.count()
        self.play_bgm(self.playingSound)
    
    def shoot(self):
        if self.mode != Scene.GAME:
            return
        if self.time == -1:
            return
        self.score += 1
        self.scoreSeg.set_value(self.score)
        self.shootSound.play()
    
    def count(self):
        if self.mode != Scene.GAME:
            return
        if self.time == -1:
            self.playingSound.stop()
            receipt.score_draw(self.score)
            self.show_score()
            return
        self.timeSeg.set_value(self.time)
        self.time -= 1
        app.after(1000, self.count)

    blink = 0
    def show_score(self):
        self.scoreSeg.set_on(self.blink % 2 == 0)
        if self.blink == 6:
            self.blink = 0
            self.record()
            return
        self.blink += 1
        app.after(250, self.show_score)
    
    def play_bgm(self, sound):
        pygame.mixer.stop()
        sound.play(-1)

    def communication(self):
        command = ser.readline().strip()
        if len(command) > 0:
            if command == b'B':
                self.start()
            elif command == b'A':
                self.shoot()
            elif command == b'C':
                self.title()
        app.after(10, self.communication)

def key(event):
    if event.keysym == 'q' or event.keysym == 'Q':
        app.destroy()
    elif event.keysym == 's' or event.keysym == 'S':
        scoreboard.start()
    elif event.keysym == 'p' or event.keysym == 'P':
        scoreboard.shoot()
    elif event.keysym == 't' or event.keysym == 'T':
        scoreboard.title()
    elif event.keysym == 'c' or event.keysym == 'C':
        scoreboard.time = 3

if __name__ == "__main__":
    global scoreboard
    if len(sys.argv) == 2:
        ser = serial.Serial(sys.argv[1], 115200, timeout=0)
    app.attributes('-fullscreen', True)
    pygame.init()
    scoreboard = ScoreBoard(app)
    scoreboard.grid()
    app.grid_columnconfigure(0, weight=1)
    app.bind('<KeyPress>', key)
    app.mainloop()
