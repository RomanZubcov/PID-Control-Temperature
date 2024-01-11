#include <DHT.h>

#define DHTPIN 2     // DHT-11 sensor output pin
#define DHTTYPE DHT11  // DHT11 sensor type
const int mosfetPin = 9; // Digital pin connected to the HW-042 module
DHT dht(DHTPIN, DHTTYPE);

// PID constants
float kp = 1;  // Proportional constant
float ki = 0.1; // Integral constant
float kd = 0.1;   // Derivative constant

// PID variables
float setpoint = 28.5;  // Setpoint temperature
float error, lastError, integral, derivative, output;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(mosfetPin, OUTPUT);

  // Wait for Serial Monitor to open
  while (!Serial);

  // Send a header to Serial Monitor
  Serial.println("Temperature(°C)\t\tPID Output");

  // Wait for a short pause to allow Serial Monitor to fully open
  delay(1000);
}

void loop() {
  // Check if there is data available for reading
  if (Serial.available() > 0) {
    // Read the command from Python
    char command = Serial.read();

    // Check the received command
    switch (command) {
      case 'R':
        // Command to send the temperature
        float temperature = dht.readTemperature();
        Serial.print("Temperature:");
        Serial.println(temperature);
        break;

      case 'S':
        // Command to update the setpoint
        setpoint = Serial.parseFloat();
        Serial.print("Setpoint updated to:");
        Serial.println(setpoint);
        break;

      // Other commands can be added here based on requirements
    }
  }

  // The rest of the code remains unchanged
  delay(1000);  // Pause between readings

  float temperature = dht.readTemperature();

  // Check if the reading failed and exit early (to try again).
  if (isnan(temperature)) {
    Serial.println("Failed to read temperature from DHT sensor!");
    return;
  }

  // Calculate PID terms
  error = setpoint - temperature;
  integral += error;
  derivative = error - lastError;

  // Calculate PID output
  output = kp * error + ki * integral + kd * derivative;

  // Control the HW-042 module based on the temperature reading and PID output
  if (output > 0) {
    // If PID output is positive, turn on the module
    digitalWrite(mosfetPin, HIGH);
  } else {
    // If PID output is negative or zero, turn off the module
    digitalWrite(mosfetPin, LOW);
  }

  // Send temperature and PID output through the serial port
  Serial.print(temperature);
  Serial.print("\t\t\t");
  Serial.println(output);

  // Update last error for the next iteration
  lastError = error;
}
