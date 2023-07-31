import sys
import ctypes
import tkinter.messagebox as messagebox
from new_f import App 
from blocker import ProcessKiller

# Check if script is running with admin rights
if not ctypes.windll.shell32.IsUserAnAdmin():
    print("Script not running with admin rights, relaunching...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Create a Tkinter window and start the UI
if __name__ == "__main__":
    app = App()  
    app.mainloop()