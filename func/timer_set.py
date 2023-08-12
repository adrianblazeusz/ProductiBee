import time
import  threading

class Timer:
    def __init__(self):
        self.total_seconds = 0
        self.is_running = False
        self.display_label = None
        self.timer_thread = None
        self.stop_event = threading.Event()

    def set_display_label(self, label):
        self.display_label = label

    def set_timer(self, time_str):
        try:
            hours, minutes = map(int, time_str.split(':'))
            self.total_seconds = hours * 3600 + minutes * 60
            self.update_display()  # Aktualizuj wyświetlany czas po ustawieniu nowego czasu
        except ValueError:
            try:
                self.total_seconds = int(time_str) * 60
                self.update_display()  # Aktualizuj wyświetlany czas po ustawieniu nowego czasu
            except ValueError:
                print("Invalid time format. Please use 'hh:mm' or 'mm'.")

    def start_timer(self):
        if self.total_seconds <= 0:
            print("Timer not set. Please set the timer first.")
            return

        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.timer_thread = threading.Thread(target=self._countdown)
            self.timer_thread.start()

    def stop_timer(self):
        if self.is_running:
            self.stop_event.set()
            self.timer_thread.join()
            self.is_running = False

    def _countdown(self):
        while self.total_seconds and not self.stop_event.is_set():
            mins, secs = divmod(self.total_seconds, 60)
            hours, mins = divmod(mins, 60)
            timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            self.total_seconds -= 1

        self.is_running = False
        if self.display_label is not None:
            self.display_label.configure(text="Time's up!")

    def update_display(self):
        if self.display_label is not None:
            mins, secs = divmod(self.total_seconds, 60)
            hours, mins = divmod(mins, 60)
            timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
            self.display_label.configure(text=timeformat)
        


