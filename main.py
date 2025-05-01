import tkinter as tk
from gui import ArduinoGUI

if __name__ == "__main__":
    root = tk.Tk()
    arduino_gui = ArduinoGUI(root)
    root.protocol("WM_DELETE_WINDOW", arduino_gui.toggle_connection)
    root.mainloop()
