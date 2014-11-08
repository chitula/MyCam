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
long dlymilUpdate = 500;

void loop() {
	int x_error;
	int y_error;

	if (Serial.available()) {
		for (int i = 0; i < numServos; i++) {
//			error[i] = constrain(Serial.read() - '0', -10, 10);
			
			char errorSign = Serial.read();
			// while(!Serial.available()) {
			// 	//Stall
			// };
			delay(50);

			char errorVal = Serial.read();
			// Ignore invalid errorVal values (outside range 0-9)
			if (errorVal < '0' || errorVal > '9') {
				errorVal = '0';
			}

			if (errorSign == '+') {
				error[i] = errorVal - '0';
			} else {
				error[i] = -(errorVal - '0');
			}

			Serial.print("errorSign[X] = ");
			Serial.println(errorSign);
			Serial.print("errorVal[X] = ");
			Serial.println(errorVal);

			Serial.print("error[");
			Serial.print(i == X ? "X" : "Y");
			Serial.print("] = ");
			Serial.println(error[i]);
		}

	}

	// Update the servo's position
	cmilUpdate = millis();
	if (dlymilUpdate < cmilUpdate - pmilUpdate) {
		for (int i = 0; i < numServos; i++) {
			current_pos[i] += error[i];
			current_pos[i] = constrain(current_pos[i], 20, 160);
			servo[i].write(current_pos[i]);

			// Print the servo ID and it's position
			Serial.print("Servo[");
			Serial.print(i);
			Serial.print("] pos = ");
			Serial.println(current_pos[i]);
		}
		pmilUpdate = cmilUpdate;
	}

}

