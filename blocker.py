import sys
import ctypes
from time import sleep
from threading import Thread
import psutil
from datetime import datetime, time
from datetime import datetime

class ProcessKiller:
    def __init__(self):
        self.active = False
        self.processes_to_kill = {"ScreenToGif.exe", "Spotify.exe"}
        self.time_range_start = None
        self.time_range_end = None
        self.thread = None
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.redirect = "127.0.0.1"
        self.sites_to_block = {"www.facebook.com","facebook.com"}

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            self.log("Blocking already running")
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
            self.log("The blocker doesn't work")

    def set_blocked_processes(self, processes):
        self.processes_to_kill = set(processes)

    def set_inactive_time_range(self, start_hour, start_minute, end_hour, end_minute):
        self.time_range_start = time(start_hour, start_minute)
        self.time_range_end = time(end_hour, end_minute)

    def block_sites(self):
        now = datetime.now().time()
        if not self.time_range_start <= now <= self.time_range_end:
            with open(self.hosts_path, 'r+') as hostfile:
                host_content = hostfile.read()
                for site in self.sites_to_block:
                    if site not in host_content:
                        hostfile.write(self.redirect + " " + site + "\n")

        else:
            with open(self.hosts_path, 'r+') as hostfile:
                lines = hostfile.readlines()
                hostfile.seek(0)
                for line in lines:
                    if not any(site in line for site in self.sites_to_block):
                        hostfile.write(line)
                hostfile.truncate()

    def kill_processes(self):
        while self.active:
            now = datetime.now().time()
            if not self.time_range_start <= now <= self.time_range_end:
                for proc in psutil.process_iter():
                    try:
                        if proc.name() in self.processes_to_kill:
                            proc.kill()
                            self.log(f"Successfully blocked {proc.name()}")
                    except psutil.NoSuchProcess:
                        pass

            self.block_sites()
                
            sleep(1)

    def log(self, message):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] {message}"
        print(message)
        if self.log_var is not None:
            log_text = self.log_var.get().split('\n')
            log_text = log_text[-5:]
            log_text.append(message)
            self.log_var.set('\n'.join(log_text))
            with open("process_killer_log.txt", "a") as f:
                f.write(message + "\n")
