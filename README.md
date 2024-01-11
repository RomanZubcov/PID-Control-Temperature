# Arduino PID Temperature Control with DHT Sensor

This Arduino project implements a Proportional-Integral-Derivative (PID) temperature control system using a DHT11 sensor to measure temperature. The system controls a MOSFET module (HW-042) to adjust the temperature based on a predefined setpoint.

# Components Required:
Arduino board
DHT11 sensor
HW-042 MOSFET module
Connection cables
Breadboard

# PID Constants:
Adjust the PID constants (kp, ki, kd) according to your specific requirements.
float kp = 1;    // Proportional constant
float ki = 0.1;  // Integral constant
float kd = 0.1;  // Derivative constant

# Notes:
The PID algorithm calculates the appropriate output to control the MOSFET module.
The system continuously monitors the temperature, adjusting the MOSFET module to maintain the desired setpoint.
