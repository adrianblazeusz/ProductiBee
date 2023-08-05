import psutil
from threading import Thread, Event
from time import sleep
from datetime import datetime
from blocker_web import Web_blocker
from json_manager import JSONManager

class ProcessKiller:
    def __init__(self):
        self.processes_to_kill = set()
        self.site_to_kill = set() 
        self.thread = None
        self.log_file = "log/process_killer_log.txt"
        self.state_file = "log/process_killer_state.json"
        self.web_blocker = Web_blocker()
        self.json_m = JSONManager(self.state_file)
        self.stop_event = Event()

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            self.log("Blocking is already running")
            return
        
        self.json_m.load_state()
        self.json_m.set_active(True)  
        self.json_m.save_state()  

        self.stop_event.clear()  # Reset the Event when starting
        self.thread = Thread(target=self.kill_processes)
        self.thread.start()
        self.log("Blocking has started")

    def stop(self):
        self.stop_event.set()  # Set the Event to stop the thread

        self.json_m.set_active(False)
        self.json_m.save_state()
        
        self.log("Blocking stopped")


    def set_blocked_processes(self, processes, add_new=True):
        if add_new:
            self.processes_to_kill.update(processes)  
        else:
            self.processes_to_kill = set(processes)

    def kill_processes(self):
        while not self.stop_event.is_set():  # Use the Event to control the loop
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


