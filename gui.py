import tkinter as tk
from arduino_controller import ArduinoController
import threading

class ArduinoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Arduino Command Sender")

        self.arduino = ArduinoController()
        
        self.label = tk.Label(master, text="Enter Command:")
        self.label.pack()

        self.command_entry = tk.Entry(master)
        self.command_entry.pack()

        self.send_button = tk.Button(master, text="Send Command", command=self.send_command)
        self.send_button.pack()

        self.response_label = tk.Label(master, text="")
        self.response_label.pack()

        self.history_label = tk.Label(master, text="Command History:")
        self.history_label.pack()

        self.history_listbox = tk.Listbox(master)
        self.history_listbox.pack()

        self.connect_button = tk.Button(master, text="Connect", command=self.toggle_connection)
        self.connect_button.pack()

        self.status_label = tk.Label(master, text="Status: Disconnected", fg="red")
        self.status_label.pack()

        self.status_light = tk.Frame(master, width=50, height=50, bg="red")
        self.status_light.pack(pady=10)

        self.running_button = tk.Button(master, text="Set Running", command=self.set_running)
        self.running_button.pack()

        self.standby_button = tk.Button(master, text="Set Standby", command=self.set_standby)
        self.standby_button.pack()

        self.stopped_button = tk.Button(master, text="Set Stopped", command=self.set_stopped)
        self.stopped_button.pack()

        self.servo_label = tk.Label(master, text="Servo Control")
        self.servo_label.pack()

        self.left_button = tk.Button(master, text="← Left", command=lambda: self.move_servo('LEFT'))
        self.left_button.pack()

        self.right_button = tk.Button(master, text="Right →", command=lambda: self.move_servo('RIGHT'))
        self.right_button.pack()

        for angle in [45, 90, 180, 360]:
            tk.Button(master, text=f"Move to {angle}°", command=lambda a=angle: self.move_servo(str(a))).pack()

        self.continuous_left = tk.Button(master, text="Continuous Left", command=lambda: self.move_servo("LEFT_LOOP"))
        self.continuous_left.pack()

        self.continuous_right = tk.Button(master, text="Continuous Right", command=lambda: self.move_servo("RIGHT_LOOP"))
        self.continuous_right.pack()

        self.servo_stop = tk.Button(master, text="Stop Servo", command=self.stop_servo)
        self.servo_stop.pack()

        self.estop_button = tk.Button(master, text="E-STOP", fg="white", bg="red", command=self.estop)
        self.estop_button.pack()

        self.reset_button = tk.Button(master, text="Reset E-STOP", command=self.reset_estop)
        self.reset_button.pack()

        self.estop_active = False

    def toggle_connection(self):
        if not self.arduino.is_connected:
            if self.arduino.connect():
                self.status_label.config(text="Status: Connected", fg="green")
                self.connect_button.config(text="Disconnect")
            else:
                self.response_label.config(text="Connection Failed")
        else:
            self.arduino.disconnect()
            self.status_label.config(text="Status: Disconnected", fg="red")
            self.connect_button.config(text="Connect")

    def send_command(self):
        if self.arduino.is_connected:
            command = self.command_entry.get()
            self.arduino.send_command(command)
            self.history_listbox.insert(tk.END, command)
            self.response_label.config(text=f"Sent: {command}")
            self.command_entry.delete(0, tk.END)
            threading.Thread(target=self.read_response).start()
        else:
            self.response_label.config(text="Error: Not connected to Arduino")

    def read_response(self):
        response = self.arduino.read_response()
        if response:
            self.response_label.config(text=f"Response: {response}")

    def set_running(self):
        if self.arduino.is_connected and not self.estop_active:
            self.arduino.send_command('RUN')
            self.status_light.config(bg="green")
            self.status_label.config(text="Status: Running", fg="green")

    def set_standby(self):
        if self.arduino.is_connected and not self.estop_active:
            self.arduino.send_command('STANDBY')
            self.status_light.config(bg="yellow")
            self.status_label.config(text="Status: Standby", fg="yellow")

    def set_stopped(self):
        if self.arduino.is_connected and not self.estop_active:
            self.arduino.send_command('STOP')
            self.status_light.config(bg="red")
            self.status_label.config(text="Status: Stopped", fg="red")

    def move_servo(self, direction):
        if self.arduino.is_connected and not self.estop_active:
            self.arduino.send_command(f"SERVO:{direction}")
            self.history_listbox.insert(tk.END, f"SERVO:{direction}")
            self.response_label.config(text=f"Sent: SERVO:{direction}")

    def stop_servo(self):
        if self.arduino.is_connected:
            self.arduino.send_command("SERVO:STOP")
            self.history_listbox.insert(tk.END, "SERVO:STOP")

    def estop(self):
        if self.arduino.is_connected:
            self.arduino.send_command("ESTOP")
            self.estop_active = True
            self.status_label.config(text="Status: E-STOP", fg="red")
            self.status_light.config(bg="red")
            self.history_listbox.insert(tk.END, "!!! E-STOP FAULT ACTIVE !!!")

    def reset_estop(self):
        if self.arduino.is_connected:
            self.arduino.send_command("RESET")
            self.estop_active = False
            self.status_label.config(text="Status: Connected", fg="green")
            self.status_light.config(bg="green")
            self.history_listbox.insert(tk.END, "E-STOP FAULT CLEARED")
