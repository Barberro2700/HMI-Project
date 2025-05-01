#include <Servo.h>

const int servoPin = 5;
Servo myServo;

int pos = 90;
bool movingLeft = false;
bool movingRight = false;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(pos);
  Serial.println("Servo Test Ready");
  Serial.println("Commands: POS 45 / POS 90 / POS 135 / POS 180 / LEFT / RIGHT / STOP");
}

void loop() {
  // Serial command handler
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "POS 45") {
      pos = 45;
      myServo.write(pos);
      Serial.println("Moved to 45°");
    } else if (cmd == "POS 90") {
      pos = 90;
      myServo.write(pos);
      Serial.println("Moved to 90°");
    } else if (cmd == "POS 135") {
      pos = 135;
      myServo.write(pos);
      Serial.println("Moved to 135°");
    } else if (cmd == "POS 180") {
      pos = 180;
      myServo.write(pos);
      Serial.println("Moved to 180°");
    } else if (cmd == "LEFT") {
      movingLeft = true;
      movingRight = false;
      Serial.println("Moving left...");
    } else if (cmd == "RIGHT") {
      movingRight = true;
      movingLeft = false;
      Serial.println("Moving right...");
    } else if (cmd == "STOP") {
      movingLeft = false;
      movingRight = false;
      Serial.println("Stopped");
    }
  }

  // Continuous movement
  if (movingLeft && pos > 0) {
    pos--;
    myServo.write(pos);
    delay(15);
  } else if (movingRight && pos < 180) {
    pos++;
    myServo.write(pos);
    delay(15);
  }
}
