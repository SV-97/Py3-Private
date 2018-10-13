import tkinter
import cv2
import numpy as np
from os import remove
from tempfile import gettempdir
from pathlib import Path

class MyApp(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.pathEntry = tkinter.Entry(self)
        self.pathEntry.pack()
        self.path = tkinter.StringVar()
        self.path.set("Path to image (e.g. .png)")
        self.pathEntry["textvariable"] = self.path
        self.close = tkinter.Button(self)
        self.close["text"] = "Quit"
        self.close["command"] = self.quit
        self.close.pack(side="right")
        self.open = tkinter.Button(self)
        self.open["text"] = "Open picture"
        self.open["command"] = self.draw_image
        self.open.pack(side="right")        
        self.cv = tkinter.Canvas(self, height=1080, width=19/9*1080)
        self.cv.pack()

    def draw_image(self):
        image = cv2.imread(self.path.get())
        height, width = image.shape[:2]
        cv_height = self.cv.winfo_height()
        cv_width = self.cv.winfo_width()
        width_offset = (cv_width - width)//2
        height_offset = (cv_height - height)//2
        padded_image = np.ones((cv_height, cv_width, 3))
        padded_image[height_offset:height+height_offset, width_offset:width+width_offset] += image
        temp_image = str(Path(gettempdir() + "/.P3_039.png")) 
        cv2.imwrite(temp_image, padded_image)
        self.image = tkinter.PhotoImage(file=temp_image)
        self.cv.create_image(0, 0, image=self.image, anchor="nw")
        remove(temp_image)

root = tkinter.Tk()
app = MyApp(root)
app.mainloop()