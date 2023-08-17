import sys
import os
import ctypes
from app import App 


if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
# Check if script is running with admin rights
if not ctypes.windll.shell32.IsUserAnAdmin():
    print("Script not running with admin rights, relaunching...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Hide the additional terminal window (stdout) when running the script
if sys.stdout is not None:
    sys.stdout = open(os.devnull, "w")

# Create a Tkinter window and start the UI
if __name__ == "__main__":
    app = App()  
    app.mainloop()