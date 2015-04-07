/*
Author: Keydrain
*/
 
#include "Arduino.h"
 
void setup()
{
  Serial.begin(9600); 
}
 
void loop()
{
  // read A0
  int val1 = analogRead(A0);
  // print to serial
  Serial.print(val1);
  Serial.print("\n");
  // Resolution of deciseconds
  delay(100);
}