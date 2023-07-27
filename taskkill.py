import os
import sys
import ctypes
from time import sleep
from threading import Thread
import psutil
import tkinter as tk
from datetime import datetime

class ProcessKiller:
    def __init__(self):
        self.active = False
        self.processes_to_kill = {"ScreenToGif.exe","Discord.exe"}
        self.thread = None

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

    def kill_processes(self):
        while self.active:
            for proc in psutil.process_iter():
                try:
                    if proc.name() in self.processes_to_kill:
                        proc.kill()
                        self.log(f"Successfully block {proc.name()}")
                except psutil.NoSuchProcess:
                    pass
            sleep(1)


    def log(self, message):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] {message}"
        print(message)
        if self.log_var is not None:
            # Split the current log text into separate lines
            log_text = self.log_var.get().split('\n')
            # Keep only the last 5 lines of the log
            log_text = log_text[-5:]
            # Add the new message to the end of the log
            log_text.append(message)
            # Update the log area with the updated log text
            self.log_var.set('\n'.join(log_text))
            # Write the log message to a text file
            with open("process_killer_log.txt", "a") as f:
                f.write(message + "\n")

class App:
    def __init__(self, master):
        self.master = master
        master.title("Blocker")

        # Create log area
        self.log_var = tk.StringVar()
        self.log_var.set("Start working!\n")
        self.log_label = tk.Label(master, textvariable=self.log_var, justify="left")
        self.log_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Create start button
        self.start_button = tk.Button(master, text="Start blocking", command=self.start_process_killer)
        self.start_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Create stop button
        self.stop_button = tk.Button(master, text="Stop blocking", command=self.stop_process_killer, state="disabled")
        self.stop_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    def start_process_killer(self):
        self.process_killer = ProcessKiller()
        self.process_killer.log_var = self.log_var
        self.process_killer.start()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_process_killer(self):
        self.process_killer.stop()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

# Check if script is running with admin rights
if not ctypes.windll.shell32.IsUserAnAdmin():
    print("Script not running with admin rights, relaunching...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Create a Tkinter window and start the UI
root = tk.Tk()
app = App(root)
root.mainloop()