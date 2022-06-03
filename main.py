import tkinter as tk
import tkinter.font as tkFont
import json

app = tk.Tk()

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

class ScoreBoard(tk.Frame):
    titleFont = tkFont.Font(family="PixelMplus12", size=100)
    segFont = tkFont.Font(family="DSEG7 Classic Bold Italic", size=32)
    
    score = 122
    time = 180
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.data = self.load_data()

        self.titleFrame = tk.Frame(self)
        self.titleFrame.grid(row=0, column=0, sticky="new")

        self.titleLabel = tk.Label(self.titleFrame, text="SHOOTING GAME", font=self.titleFont)
        self.titleLabel.grid(column=1, row=0)

        self.scoreSeg = SegWithTitle(self, "SCORE", self.score, height=200)
        self.scoreSeg.grid(column=0, row=4)
        
        self.subFrame = tk.Frame(self)
        self.subFrame.grid(column=0, row=5)
        self.subFrame.grid_columnconfigure(0, weight=1)
        self.subFrame.grid_columnconfigure(3, weight=1)

        self.recordSeg = SegWithTitle(self.subFrame, "RECORD", self.data['record'], height=100, color="#00ff1e", background="#003606")
        self.recordSeg.grid(column=0, row=0, sticky=tk.NE)
        
        self.timeSeg = SegWithTitle(self.subFrame, "TIME", self.time, height=100, color="#ffe100", background="#2e2900")
        self.timeSeg.grid(column=2, row=0, sticky=tk.NE)

        self.count()
        self.title()

    index = 0
    title_text = '!!!PRES!BTN!!'
    def title(self):
        if self.index == len(self.title_text) - 1:
            self.index = 0
        self.scoreSeg.set_value(self.title_text[self.index:self.index + 3])
        self.index += 1
        app.after(300, self.title)
    
    def load_data(self):
        data = { "record": 0 }
        try:
            with open('./data.json', 'r') as f:
                data = json.load(f)
        except:
            pass
        return data

    def count(self):
        if self.time == -1:
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
            return
        self.blink += 1
        app.after(250, self.show_score)


def quit(event):
    if event.keysym == 'q' or event.keysym == 'Q':
        app.destroy()

if __name__ == "__main__":
    app.attributes('-fullscreen', True)
    ScoreBoard(app).grid()
    app.grid_columnconfigure(0, weight=1)
    app.bind('<KeyPress>', quit)
    app.mainloop()
