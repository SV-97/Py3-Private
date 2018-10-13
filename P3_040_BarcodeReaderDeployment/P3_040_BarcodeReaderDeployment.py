from threading import Lock
import tkinter

import backend
import ui

lock = Lock()
shutdown = [False]
image = []
backend = backend.ReadCode(image, lock, exit)
backend.start()
ui = ui.UIThread(lock, image, exit)
ui.start()
threads = (ui, backend)

while True:
    for thread in threads:
        if not thread.is_alive():
            shutdown[0] = True
            thread.join()
