from os import remove
from pathlib import Path
from sys import stderr
from tempfile import gettempdir
import threading

import cv2
import numpy as np
import tkinter

from shared_classes import KillableThread

class NamedTempFile():
    """Context Manager for temporary files with user-setable name
    Creates a file on entering and removes it on leaving.
    """
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.file = open(self.name, "w")
        self.file.close()
    def __exit__(self, exc_type, exc_value, traceback):
        remove(self.name)

class Main(tkinter.Frame):
    def __init__(self, image, lock, master=None):
        super().__init__(master)
        self.pack()
        self.lock = lock
        self.image = image
        self.create_widgets()

    def create_widgets(self):
        self.close = tkinter.Button(self)
        self.close["text"] = "Quit"
        def quit():
            stderr.write("Aborted")
            self.quit
        self.close["command"] = quit
        self.close.pack(side="right")     
        height = 640
        self.cv = tkinter.Canvas(self, height=height, width=16/9*height)
        self.cv.pack()
        self.draw_image()

    def draw_image(self):
        """if self.should_i_die():
            return"""
        if self.image:
            with self.lock:
                image = self.image[0]
            height, width = image.shape[:2]
            """
            cv_height = self.cv.winfo_height()
            cv_width = self.cv.winfo_width()
            width_offset = (cv_width - width)//2
            height_offset = (cv_height - height)//2
            padded_image = np.ones((cv_height, cv_width, 3))
            padded_image[height_offset:height+height_offset, width_offset:width+width_offset] += image
            temp_image = str(Path(gettempdir() + "/.P3_039.png")) 
            with NamedTempFile(temp_image):
                cv2.imwrite(temp_image, padded_image)
                self.photo_image = tkinter.PhotoImage(file=temp_image)
                self.cv.create_image(0, 0, image=self.photo_image, anchor="nw")
            """
                
            temp_image = str(Path(gettempdir() + "/.P3_039.png")) 
            with NamedTempFile(temp_image):
                cv2.imwrite(temp_image, image)
                self.photo_image = tkinter.PhotoImage(file=temp_image)
                self.cv.create_image(0, 0, image=self.photo_image, anchor="nw")
        self.master.after(20, self.draw_image)
        
class UIThread(KillableThread):
    def __init__(self, image, lock):
        super().__init__(daemon=True)
        self.name = "UI"
        self.lock = lock
        self.image = image
    def run(self):
        root = tkinter.Tk()
        root.title("SV Barcode Reader")
        app = Main(self.image, self.lock, root)
        def healthcheck():
            if self.should_i_die():
                return
        root.after(20, healthcheck)
        app.mainloop()