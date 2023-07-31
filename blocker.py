from time import sleep
from threading import Thread
import psutil
from datetime import datetime


class ProcessKiller:
    def __init__(self):
        self.active = False
        self.processes_to_kill = set()
        self.sites_to_block = set()
        self.thread = None
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.redirect = "127.0.0.1"

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

    def set_blocked_websites(self, websites):
        self.sites_to_block = set(websites)

    def block_sites(self):
        if self.active:
            with open(self.hosts_path, 'r+') as hostfile:
                host_content = hostfile.read()
                for site in self.sites_to_block:
                    if site not in host_content:
                        hostfile.write(self.redirect + " " + site + "\n")
        else:
            self.unblock_sites()

    def unblock_sites(self):
        with open(self.hosts_path, 'r+') as hostfile:
            lines = hostfile.readlines()
            hostfile.seek(0)
            for line in lines:
                if not any(site in line for site in self.sites_to_block):
                    hostfile.write(line)
            hostfile.truncate()

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
        self.block_sites()

    def log(self, message):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{current_time}] {message}"
        print(log_message)
        with open("process_killer_log.txt", "a") as f:
            f.write(log_message + "\n")

