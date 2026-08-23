#include <Stepper.h>

// Define the number of steps per revolution for your specific motor (e.g., 200)
const int stepsPerRevolution = 200;

// Map Romeo V1.3 direction pins to the library
// Pin 4 = Motor 1 Direction, Pin 7 = Motor 2 Direction
// We pass dummy pins (8, 9) because the library expects 4 pins, but we only use 2 for direction control
Stepper myStepper(stepsPerRevolution, 4, 8, 7, 9);

// Romeo Enable/Speed pins
const int M1_PWM = 5;
const int M2_PWM = 6;

void setup() {
  Serial.begin(9600);
  // Set Romeo driver enable pins as outputs
  pinMode(M1_PWM, OUTPUT);
  pinMode(M2_PWM, OUTPUT);
  
  // Keep driver channels permanently enabled
  digitalWrite(M1_PWM, HIGH);
  digitalWrite(M2_PWM, HIGH);

  // Set motor speed in RPM
  myStepper.setSpeed(60);
}

void loop() {
    if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      myStepper.step(stepsPerRevolution);
      delay(1000);
    } else if (command == '0') {
      myStepper.step(-stepsPerRevolution);
      delay(1000);
    }
  }
}