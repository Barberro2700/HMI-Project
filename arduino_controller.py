import serial
import time

class ArduinoController:
    def __init__(self, port='COM11', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None
        self.is_connected = False

    def connect(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baudrate)
            time.sleep(2)  # Wait for the connection to establish
            self.is_connected = True
            return True
        except Exception as e:
            print(f"Connection Error: {e}")
            return False

    def disconnect(self):
        if self.serial_port:
            self.serial_port.close()
            self.is_connected = False

    def send_command(self, command):
        if self.is_connected:
            self.serial_port.write(command.encode())

    def read_response(self):
        if self.is_connected and self.serial_port.in_waiting > 0:
            return self.serial_port.readline().decode('utf-8').strip()
        return None