/*
Author: Keydrain
*/
 
#include "Arduino.h"
#include <Stepper.h>

// Pins for Stepper motor setup.
int in1Pin = 12;
int in2Pin = 11;
int in3Pin = 10;
int in4Pin = 9;
// integer for tracking number of beads.
int beads = 0;

// Stepper step definition and pin mapping. 
Stepper motor(200, in1Pin, in2Pin, in3Pin, in4Pin);
 
void setup()
{
 
  // Stepper pin linking.
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(in3Pin, OUTPUT);
  pinMode(in4Pin, OUTPUT);
 
  Serial.begin(9600); 
  // setTimeout makes the port much faster than default. 
  Serial.setTimeout(10); 
  motor.setSpeed(40); // 20 is technically safe max.
  
}
 
void loop()
{
  // read A0, the salinity probe voltage divider.
  int salt = analogRead(A0);
  // print to serial
  Serial.println(salt);
  
  if (Serial.available()) {
    // read Serial input as integer.
    beads = Serial.parseInt();
    // *5 is for speed setting. See motor.step(10);
    beads = beads*5;
  }
  if (beads > 0) {
    // 10 is for speed setting. See beads = beads*5;
    motor.step(10);
    // decrements the bead counter to not block the reader.
    beads = beads-1;
  } else {
    // If not running motor, then add some delay to match that decisecond timing. 
    delay(100);
  }
  
}
