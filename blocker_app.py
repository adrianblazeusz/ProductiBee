import os
import json
import psutil
from threading import Thread
from time import sleep
from datetime import datetime

class ProcessKiller:
    def __init__(self):
        self.active = False
        self.processes_to_kill = set()
        self.thread = None
        self.log_file = "log/process_killer_log.txt"
        self.state_file = "log/process_killer_state.json"

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

    def set_blocked_processes(self, processes, add_new=True):
        if add_new:
            self.processes_to_kill.update(processes)  
        else:
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
        with open(self.log_file, "a") as f:
            f.write(log_message + "\n")

    def save_state(self):
        state = {
            "active": self.active,
            "processes_to_kill": list(self.processes_to_kill),
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                state = json.load(f)
                self.active = state.get("active", False)
                self.processes_to_kill = set(state.get("processes_to_kill", []))

