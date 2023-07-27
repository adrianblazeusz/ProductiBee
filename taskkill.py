import sys
import ctypes
from time import sleep
from threading import Thread
import psutil
import tkinter as tk
from datetime import datetime, time

class ProcessKiller:
    def __init__(self):
        self.active = False
        self.processes_to_kill = {"ScreenToGif.exe", "Discord.exe"}
        self.time_range_start = None
        self.time_range_end = None
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

    def set_inactive_time_range(self, start_hour, start_minute, end_hour, end_minute):
        self.time_range_start = time(start_hour, start_minute)
        self.time_range_end = time(end_hour, end_minute)

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

class App:
    def __init__(self, master):
        self.master = master
        master.title("Blocker")

        # Create log area
        self.log_var = tk.StringVar()
        self.log_var.set("Start working!\n")
        self.log_label = tk.Label(master, textvariable=self.log_var, justify="left")
        self.log_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

          # Create inactive time range input fields
        self.inactive_start_hour_var = tk.StringVar()
        self.inactive_start_minute_var = tk.StringVar()
        self.inactive_end_hour_var = tk.StringVar()
        self.inactive_end_minute_var = tk.StringVar()

        self.inactive_start_hour_var.set("17")
        self.inactive_start_minute_var.set("0")
        self.inactive_end_hour_var.set("17")
        self.inactive_end_minute_var.set("30")

        self.inactive_start_hour_label = tk.Label(master, text="Inactive Start Hour:")
        self.inactive_start_hour_label.grid(row=4, column=0, padx=10, pady=2, sticky="w")
        self.inactive_start_hour_entry = tk.Entry(master, textvariable=self.inactive_start_hour_var, width=4)
        self.inactive_start_hour_entry.grid(row=4, column=1, padx=2, pady=2, sticky="w")

        self.inactive_start_minute_label = tk.Label(master, text="Inactive Start Minute:")
        self.inactive_start_minute_label.grid(row=4, column=2, padx=10, pady=2, sticky="w")
        self.inactive_start_minute_entry = tk.Entry(master, textvariable=self.inactive_start_minute_var, width=4)
        self.inactive_start_minute_entry.grid(row=4, column=3, padx=2, pady=2, sticky="w")

        self.inactive_end_hour_label = tk.Label(master, text="Inactive End Hour:")
        self.inactive_end_hour_label.grid(row=5, column=0, padx=10, pady=2, sticky="w")
        self.inactive_end_hour_entry = tk.Entry(master, textvariable=self.inactive_end_hour_var, width=4)
        self.inactive_end_hour_entry.grid(row=5, column=1, padx=2, pady=2, sticky="w")

        self.inactive_end_minute_label = tk.Label(master, text="Inactive End Minute:")
        self.inactive_end_minute_label.grid(row=5, column=2, padx=10, pady=2, sticky="w")
        self.inactive_end_minute_entry = tk.Entry(master, textvariable=self.inactive_end_minute_var, width=4)
        self.inactive_end_minute_entry.grid(row=5, column=3, padx=2, pady=2, sticky="w")

        # Create start button
        self.start_button = tk.Button(master, text="Start blocking", command=self.start_process_killer)
        self.start_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Create stop button
        self.stop_button = tk.Button(master, text="Stop blocking", command=self.stop_process_killer, state="disabled")
        self.stop_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    def start_process_killer(self):
        try:
            start_hour = int(self.inactive_start_hour_var.get())
            start_minute = int(self.inactive_start_minute_var.get())
            end_hour = int(self.inactive_end_hour_var.get())
            end_minute = int(self.inactive_end_minute_var.get())

            if not (0 <= start_hour <= 23 and 0 <= start_minute <= 59 and 0 <= end_hour <= 23 and 0 <= end_minute <= 59):
                raise ValueError("Invalid time format. Hours should be between 0 and 23, minutes between 0 and 59.")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
            return

        self.process_killer = ProcessKiller()
        self.process_killer.log_var = self.log_var
        self.process_killer.set_inactive_time_range(start_hour, start_minute, end_hour, end_minute)
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
