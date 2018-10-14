from threading import Lock
import tkinter

import backend
import ui
from time import sleep

lock = Lock()
image = []
backend = backend.ReadCode(image, lock)
backend.start()
ui = ui.UIThread(image, lock)
ui.start()
threads = (ui, backend)

while True:
    for thread in threads:
        if not thread.is_alive():
            thread.join()
    """if True not in map(lambda x: x.is_alive(), threads):
        break"""