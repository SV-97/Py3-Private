from threading import Thread, Event

class KillableThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._kill_event = Event()
        self._abort_event = Event()
    def kill(self):
        self._kill_event.set()
    def should_i_die(self):
        return self._kill_event.is_set()
    def abort(self):
        self._abort_event.set()
    def aborted(self):
        return self._abort_event.is_set()