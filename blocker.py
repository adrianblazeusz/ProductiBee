from time import sleep
from threading import Thread
import psutil
from datetime import datetime


class ProcessKiller:
    def __init__(self):
        self.active = False
        self.processes_to_kill = set()
        self.thread = None

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            self.log("Blocking is already running")
            return

        self.active = True
        self.thread = Thread(target=self.kill_processes)
        self.thread.start()
        self.log("Blocking has started")

    def stop(self):
        self.active = False
        if self.thread is not None:
            self.thread.join()
            self.log("Blocking stopped")
        else:
            self.log("The blocker isn't running")

    def set_blocked_processes(self, processes):
        self.processes_to_kill = set(processes)

    def kill_processes(self):
        while self.active:
            for proc in psutil.process_iter():
                try:
                    if proc.name() in self.processes_to_kill:
                        proc.kill()
                        self.log(f"Successfully blocked {proc.name()}")
                except psutil.NoSuchProcess:
                    pass
            sleep(1)
        

    def log(self, message):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{current_time}] {message}"
        print(log_message)
        with open("process_killer_log.txt", "a") as f:
            f.write(log_message + "\n")

