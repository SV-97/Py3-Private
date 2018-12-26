from threading import Lock, Thread
from time import sleep, time

class Timeout(Thread):
    """Timer that runs in background and executes a function if it's not refreshed
    Important: This is different from the threading.Timer class in that it can provide
    arguments to a function as well as allows reseting the timer, rather than cancelling
    completely.

        Args:
            function: function that is executed once time runs out
            timeout: time in seconds after which the timeout executes the function
            args: arguments for function

        Attributes:
            timeout: time in seconds afters which the timer times out
            function: function to be executed once time runs out
            args: arguments for function
            lock: mutex for various attributes
            timed_out: boolean presenting wether the timer timed out
            last_interaction_timestamp: unix timestamp of last refresh/initialization
        
        Properties:
            timer: 
    """

    def __init__(self, timeout, function, args=None):
        super().__init__()
        if args is None:
            args = []
        self.timeout = timeout
        self.function = function
        self.args = args
        self.lock = Lock()
        self.timed_out = False
        self.reset()

    def _refresh_timer(self):
        with self.lock:
            return self.timeout - (time() - self.last_interaction_timestamp)

    timer = property(fget=_refresh_timer)

    def reset(self):
        """Reset the internal timer"""
        with self.lock:
            if not self.timed_out:
                self.is_reset = True
                self.last_interaction_timestamp = time()

    def run(self):
        """Start the timer"""
        with self.lock:
            if self.is_reset:
                self.is_reset = False           
            else:
                self.timed_out = True
                self.function(*self.args)
                return
            difference_to_timeout = self.timeout - (time() - self.last_interaction_timestamp)
        sleep(difference_to_timeout)
        self.run() 


if __name__ == "__main__":
    from threading import Thread

    timeout = Timeout(timeout=10, function=print, args=["timed out"])
    timeout.start()
    reset_thread = Thread(target=lambda: timeout.reset() if input() else None) # function for testing - reset on input
    reset_thread.start()
    t = 0
    delta_t = 1
    t1 = time()
    while not timeout.timed_out:
        print(f"Not timed out yet - {t:.2f} seconds passed")
        print(timeout.timer)
        t += delta_t
        sleep(delta_t)
    print(time() - t1)
    timeout.join()
    reset_thread.join()