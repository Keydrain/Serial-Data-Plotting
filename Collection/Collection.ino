/*
Author: Keydrain
*/
 
#include "Arduino.h"
#include <Stepper.h>

int in1Pin = 12;
int in2Pin = 11;
int in3Pin = 10;
int in4Pin = 9;
int beads = 0;
//int inPumpPin = 8; // This may be needed for the pump. Not sure...

Stepper motor(200, in1Pin, in2Pin, in3Pin, in4Pin);
 
void setup()
{
 
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(in3Pin, OUTPUT);
  pinMode(in4Pin, OUTPUT);
 
  Serial.begin(9600); 
  Serial.setTimeout(10);
  motor.setSpeed(40); // 20 is technically safe max
  
}
 
void loop()
{
  
  // read A0, the salinity probe voltage divider
  int salt = analogRead(A0);
  // print to serial
  Serial.println(salt);
  
  if (Serial.available()) {
    // read Serial input as integer
    beads = Serial.parseInt();
    beads = beads*5;
  }
  if (beads > 0) {
    motor.step(10);
    beads = beads-1;
  } else {
    delay(100);
  }
  
}
