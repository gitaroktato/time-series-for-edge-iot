/**
 * Blink
 *
 * Turns on an LED on for one second,
 * then off for one second, repeatedly.
 */
#include <Arduino.h>
#define TICK_RATE 500

// Set LED_BUILTIN if it is not defined by Arduino framework
// #define LED_BUILTIN 13

bool ledState = 0x0;

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(7, INPUT_PULLUP); //set pin 7 as an input and enable the internal pull-up resistor
  Serial.begin(9600);
}

void loop()
{
  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_BUILTIN, HIGH);

  int x = analogRead(A0);	// read X axis value [0..1023]
  int y = analogRead(A1);	// read Y axis value [0..1023]
  // Joystick data - line protocol somewhat
  Serial.print("controller x=" + String(x));
  Serial.println(",y=" + String(y));

  ledState = !ledState;
  // turn the LED off by making the voltage LOW
  digitalWrite(LED_BUILTIN, ledState);

   // wait for a second
  delay(TICK_RATE);
}