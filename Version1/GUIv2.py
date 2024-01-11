import tkinter as tk
from tkinter import ttk
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PIDControllerGUI:
    def __init__(self, master):
        self.master = master
        master.title("PID Controller")

        self.current_temp_label = ttk.Label(master, text="Current Temperature: N/A")
        self.current_temp_label.grid(row=8, column=0, columnspan=4)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Temperature (°C)')
        self.ax.set_title('Temperature and PID Output')

        self.ax_pid = self.ax.twinx()
        self.ax_pid.set_ylabel('PID Output')

        self.times = []
        self.temperatures = []
        self.pid_outputs = []

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, columnspan=4)

        self.serial_connection = serial.Serial('COM4', 9600)
        master.after(1000, self.update_current_temperature)

    def update_values(self):
        try:
            kp = float(self.kp_entry.get())
            ki = float(self.ki_entry.get())
            kd = float(self.kd_entry.get())
            setpoint = float(self.setpoint_entry.get())

            values_str = f"S{setpoint:.2f}P{kp:.2f}I{ki:.2f}D{kd:.2f}\n"
            self.serial_connection.write(values_str.encode())
            print(f"Updated PID values: {values_str}")
        except ValueError:
            print("Invalid input. Please enter valid numeric values.")

    def update_setpoint(self):
        try:
            setpoint = float(self.setpoint_entry.get())
            values_str = f"S{setpoint:.2f}\n"
            self.serial_connection.write(values_str.encode())
            print(f"Updated Setpoint value: {setpoint}")
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")

    def update_current_temperature(self):
        self.serial_connection.write(b'R')
        temperature_str = "0.0"

        try:
            temperature_str = self.serial_connection.readline().decode().strip()
            temperature, pid_output = map(float, temperature_str.split("\t\t\t"))
            self.current_temp_label.config(text=f"Current Temperature: {temperature:.2f} °C, PID Output: {pid_output:.2f}")

            self.times.append(len(self.times) + 1)
            self.temperatures.append(temperature)
            self.pid_outputs.append(pid_output)

            self.ax.clear()
            self.ax.plot(self.times, self.temperatures, label='Temperature', color='blue')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Temperature (°C)')
            self.ax.legend(loc='upper left')

            self.ax_pid.clear()
            self.ax_pid.plot(self.times, self.pid_outputs, label='PID Output', color='red')
            self.ax_pid.set_ylabel('PID Output')
            self.ax_pid.legend(loc='upper right')

            self.canvas.draw()

        except ValueError:
            print(f"Invalid data received from Arduino: {temperature_str}")

        self.master.after(1000, self.update_current_temperature)

if __name__ == "__main__":
    root = tk.Tk()
    app = PIDControllerGUI(root)
    root.mainloop()
