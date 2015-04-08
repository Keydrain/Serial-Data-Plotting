/*
Author: Keydrain
*/
 
#include "Arduino.h"
#include <Stepper.h>

int in1Pin = 12;
int in2Pin = 11;
int in3Pin = 10;
int in4Pin = 9;
//int inPumpPin = 8; // This may be needed for the pump. Not sure...

Stepper motor(4, in1Pin, in2Pin, in3Pin, in4Pin);
 
void setup()
{
 
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(in3PIn, OUTPUT);
  pinMode(in4Pin, OUTPUT);
 
  Serial.begin(9600); 
  motor.setSpeed(20); // 20 is a filler for the time being. 
}
 
void loop()
{
  // read A0
  int val1 = analogRead(A0);
  // print to serial
  Serial.print(val1);
  Serial.print("\n");
  // Resolution of deciseconds
  
  /*
  motor.step(1); // This is to move one step. Needs some logic to determine when to step. 
  */
  delay(100);
}
