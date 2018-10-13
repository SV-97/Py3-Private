import tkinter
import cv2
import numpy as np
from os import remove
from tempfile import gettempdir
from pathlib import Path
import threading


class NamedTempFile():
    """Context Manager for temporary files with user-setable name
    Creates a file on entering and removes it on leaving.
    """
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.file = open(self.name, "x")
        self.file.close()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        remove(self.name)

class Main(tkinter.Frame):
    def __init__(self, lock, image, master=None):
        super().__init__(master)
        self.pack()
        self.lock = lock
        self.create_widgets()
        self.image = image

    def create_widgets(self):
        self.close = tkinter.Button(self)
        self.close["text"] = "Quit"
        self.close["command"] = self.quit
        self.close.pack(side="right")     
        self.cv = tkinter.Canvas(self, height=1080, width=19/9*1080)
        self.cv.pack()
        self.draw_image()

    def draw_image(self):
        with self.lock:
            image = self.image[0]
        height, width = image.shape[:2]
        cv_height = self.cv.winfo_height()
        cv_width = self.cv.winfo_width()
        width_offset = (cv_width - width)//2
        height_offset = (cv_height - height)//2
        padded_image = np.ones((cv_height, cv_width, 3))
        padded_image[height_offset:height+height_offset, width_offset:width+width_offset] += image
        temp_image = str(Path(gettempdir() + "/.P3_039.png")) 
        with NamedTempFile(temp_image):
            cv2.imwrite(temp_image, padded_image)
            self.image = tkinter.PhotoImage(file=temp_image)
            self.cv.create_image(0, 0, image=self.image, anchor="nw")
        self.after(1, self.draw_image)

class UIThread(threading.Thread):
    def __init__(self, lock, image):
        super().__init__()
        self.lock = lock
        self.image = image
    def run(self):
        root = tkinter.Tk()
        root.title("SV Barcode Reader")
        app = Main(root, self.lock, self.image)
        app.mainloop()