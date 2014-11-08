#include <Servo.h>

#define X 0
#define Y 1

const int numServos = 1;

Servo servo[2];
int servoPin[2] = {9, 10};

int center_pos[2] = {90, 90};
int current_pos[2];
int error[2] = {0, 0};

void setup() {
	Serial.begin(9600);

	// Align the servos at startup to the center position
	for (int i = 0; i < numServos; i++) {
		current_pos[i] = center_pos[i];
		servo[i].attach(servoPin[i]);
		servo[i].write(current_pos[i]);
	}
}


long pmilUpdate = 0;
long cmilUpdate = 0;
long dlymilUpdate = 50;

void loop() {
	int x_error;
	int y_error;

	if (Serial.available()) {
		for (int i = 0; i < numServos; i++) {
			error[i] = constrain(Serial.read(), -10, 10);
		}

	}

	// Update the servo's position
	cmilUpdate = millis();
	if (dlymilUpdate < cmilUpdate - pmilUpdate) {
		for (int i = 0; i < numServos; i++) {
			current_pos[i] += error[i];
			current_pos[i] = constrain(current_pos[i], 20, 160);
			servo[i].write(current_pos[i]);
		}
		pmilUpdate = cmilUpdate;
	}

}

