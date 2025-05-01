#include <Servo.h>

// RGB LED pins
const int redPin = 9;
const int greenPin = 10;
const int bluePin = 11;

// Claxon (buzzer) pin
const int buzzerPin = 6;

// Servo pin
const int servoPin = 5;
Servo myServo;

// State variables
bool estop_active = false;
bool movingLeft = false;
bool movingRight = false;
String system_mode = "OFF";  // Track RUN, STANDBY, STOP

int currentServoPos = 90; // neutral start
int redVal = 0, greenVal = 0, blueVal = 0;

void setup() {
  Serial.begin(9600);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  myServo.attach(servoPin);
  myServo.write(currentServoPos);

  setColor(0, 0, 0); // All off
}

void loop() {
  if (estop_active) {
    blinkEstop();
    return;
  }

  // Continuous servo movement
  if (movingLeft && currentServoPos > 0) {
    currentServoPos--;
    myServo.write(currentServoPos);
    delay(15);
  } else if (movingRight && currentServoPos < 180) {
    currentServoPos++;
    myServo.write(currentServoPos);
    delay(15);
  }

  // Handle commands
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "RUN") {
      system_mode = "RUN";
      setColor(0, 255, 0); // Green
    } else if (command == "STANDBY") {
      system_mode = "STANDBY";
      setColor(255, 255, 0); // Yellow
    } else if (command == "STOP") {
      system_mode = "STOP";
      setColor(255, 0, 0); // Red
    } else if (command == "ESTOP") {
      estop_active = true;
    } else if (command == "RESET") {
      estop_active = false;
      noTone(buzzerPin);
      restoreModeColor();
    }

    // Position commands
    else if (command == "POS 45") {
      currentServoPos = 45;
      myServo.write(currentServoPos);
    } else if (command == "POS 90") {
      currentServoPos = 90;
      myServo.write(currentServoPos);
    } else if (command == "POS 180" || command == "POS 360") {
      currentServoPos = 180;
      myServo.write(currentServoPos);
    }

    // Continuous movement
    else if (command == "LEFT") {
      movingLeft = true;
      movingRight = false;
    } else if (command == "RIGHT") {
      movingRight = true;
      movingLeft = false;
    } else if (command == "SERVO_STOP") {
      movingLeft = false;
      movingRight = false;
    }
  }
}

void setColor(int red, int green, int blue) {
  redVal = red;
  greenVal = green;
  blueVal = blue;
  analogWrite(redPin, redVal);
  analogWrite(greenPin, greenVal);
  analogWrite(bluePin, blueVal);
}

void restoreModeColor() {
  if (system_mode == "RUN") {
    setColor(0, 255, 0);
  } else if (system_mode == "STANDBY") {
    setColor(255, 255, 0);
  } else if (system_mode == "STOP") {
    setColor(255, 0, 0);
  } else {
    setColor(0, 0, 0);
  }
}

void blinkEstop() {
  setColor(255, 0, 0); // Red
  tone(buzzerPin, 1000);
  delay(300);
  setColor(0, 0, 0);
  noTone(buzzerPin);
  delay(300);
}
