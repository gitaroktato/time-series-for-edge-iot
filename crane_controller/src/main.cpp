/**
 * Crane controller driver
 */
#include <Arduino.h>
// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "I2Cdev.h"
#include "MPU6050.h"

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif
// Rate of reading sensor data
#define TICK_RATE 100
// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 mpu;
//MPU6050 accelgyro(0x69); // <-- use for AD0 high
//MPU6050 accelgyro(0x68, &Wire1); // <-- use for AD0 low, but 2nd Wire (TWI/I2C) object
int16_t accelerometer_x, accelerometer_y, accelerometer_z;
int16_t gyroscope_x, gyroscope_y, gyroscope_z;
// LED state for switching onboard LED
bool ledState = false;

void setup_gyroscope() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize device
    Serial.println("Initializing I2C devices...");
    mpu.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(mpu.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

    // use the code below to change accel/gyro offset values
    /*
    Serial.println("Updating internal sensor offsets...");
    // -76	-2359	1688	0	0	0
    Serial.print(mpu.getXAccelOffset()); Serial.print("\t"); // -76
    Serial.print(mpu.getYAccelOffset()); Serial.print("\t"); // -2359
    Serial.print(mpu.getZAccelOffset()); Serial.print("\t"); // 1688
    Serial.print(mpu.getXGyroOffset()); Serial.print("\t"); // 0
    Serial.print(mpu.getYGyroOffset()); Serial.print("\t"); // 0
    Serial.print(mpu.getZGyroOffset()); Serial.print("\t"); // 0
    Serial.print("\n");
    mpu.setXGyroOffset(220);
    mpu.setYGyroOffset(76);
    mpu.setZGyroOffset(-85);
    Serial.print(mpu.getXAccelOffset()); Serial.print("\t"); // -76
    Serial.print(mpu.getYAccelOffset()); Serial.print("\t"); // -2359
    Serial.print(mpu.getZAccelOffset()); Serial.print("\t"); // 1688
    Serial.print(mpu.getXGyroOffset()); Serial.print("\t"); // 0
    Serial.print(mpu.getYGyroOffset()); Serial.print("\t"); // 0
    Serial.print(mpu.getZGyroOffset()); Serial.print("\t"); // 0
    Serial.print("\n");
    */
}

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(7, INPUT_PULLUP); //set pin 7 as an input and enable the internal pull-up resistor
  // initialize serial communication
  // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
  // it's really up to you depending on your project)
  Serial.begin(38400);
  setup_gyroscope();
}

void read_and_print_joystick_state() {
  int x = analogRead(A0);	// read X axis value [0..1023]
  int y = analogRead(A1);	// read Y axis value [0..1023]
  // Joystick data - line protocol somewhat
  Serial.print("controller x=" + String(x));
  Serial.println(",y=" + String(y));
}

void switch_builtin_led() {
  read_and_print_joystick_state();
  ledState = !ledState;
  // turn the LED off by making the voltage LOW
  digitalWrite(LED_BUILTIN, ledState);
}

void read_and_print_gyroscope_state() {
    mpu.getAcceleration(&accelerometer_x, &accelerometer_y, &accelerometer_z);
    mpu.getRotation(&gyroscope_x, &gyroscope_y, &gyroscope_z);

    // Gyro data - line protocol somewhat
    Serial.println("accel x=" + String(accelerometer_x) + ",y=" + String(accelerometer_y) + ",z=" + String(accelerometer_z));
    Serial.println("gyro x=" + String(gyroscope_x) + ",y=" + String(gyroscope_y) + ",z=" + String(gyroscope_z));
}

void loop() {
  read_and_print_gyroscope_state();
  read_and_print_joystick_state();
   // wait for TICK_RATE
  delay(TICK_RATE);
}