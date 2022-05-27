import tkinter as tk
import tkinter.font as tkFont

app = tk.Tk()

class Seg(tk.Canvas):
    font_name = "DSEG14 Classic"
    def __init__(self, parent, height, value, color, background):
        font = (self.font_name, height)

        pad = height * 0.1
        pad_bottom = 2 * pad

        info = tkFont.Font(family=self.font_name, size=height)
        value_len = len(str(value))
        width = value_len * info.measure("m")
        tk.Canvas.__init__(self, parent, width=width + pad * 2, height=height + pad + pad_bottom, background="black")
        self.create_text(pad, pad, text="".join(['~' for _ in range(value_len)]), fill=background, font=font, anchor=tk.NW)
        self.create_text(pad, pad, text=value, fill=color, font=font, anchor=tk.NW)

class SegWithTitle(tk.Frame):
    def __init__(self, parent, title, value, height=100, color="red", background="#310000"):
        tk.Frame.__init__(self, parent)
        seg = Seg(self, height, value, color, background)
        seg.grid(column=0, row=0)
        titleFont = tkFont.Font(family="PixelMplus12", size=int(height * 0.3))
        title = tk.Label(self, text=title, font=titleFont)
        title.grid(column=0, row=1)

class ScoreBoard(tk.Frame):
    titleFont = tkFont.Font(family="PixelMplus12", size=100)
    segFont = tkFont.Font(family="DSEG7 Classic Bold Italic", size=32)
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.titleFrame = tk.Frame(self)
        self.titleFrame.grid(row=0, column=0, sticky="new")

        self.titleLabel = tk.Label(self.titleFrame, text="SHOOTING GAME", font=self.titleFont)
        self.titleLabel.grid(column=1, row=0)

        self.scoreSeg = SegWithTitle(self, "SCORE", 100, height=200)
        self.scoreSeg.grid(column=0, row=4)

        self.subFrame = tk.Frame(self)
        self.subFrame.grid(column=0, row=5)
        self.subFrame.grid_columnconfigure(0, weight=1)
        self.subFrame.grid_columnconfigure(3, weight=1)

        self.recordSeg = SegWithTitle(self.subFrame, "RECORD", 100, height=100, color="#00ff1e", background="#003606")
        self.recordSeg.grid(column=0, row=0, sticky=tk.NE)

        self.timeSeg = SegWithTitle(self.subFrame, "TIME", 100, height=100, color="#ffe100", background="#2e2900")
        self.timeSeg.grid(column=2, row=0, sticky=tk.NE)


if __name__ == "__main__":
    app.attributes('-fullscreen', True)
    ScoreBoard(app).grid()
    app.grid_columnconfigure(0, weight=1)
    app.mainloop()
