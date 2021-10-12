// ---------------------------------------------------------------------------
// By: Liam Mahoney and Aaron Roitman
// Example NewPing library sketch that does a ping about 20 times per second.
// ---------------------------------------------------------------------------
// include the library code
#include "NewPing.h"
#include <stdio.h>
#include <time.h>


#define TRIGGER_PIN_1  3  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN_1     2  // Arduino pin tied to echo pin on the ultrasonic sensor.

#define TRIGGER_PIN_2  5  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN_2     4  // Arduino pin tied to echo pin on the ultrasonic sensor.

#define TRIGGER_PIN_3  9  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN_3     8  // Arduino pin tied to echo pin on the ultrasonic sensor.

#define MAX_DISTANCE 250 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar1(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar3(TRIGGER_PIN_3, ECHO_PIN_3, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

const int numReadings = 3;
float readings1[numReadings];      // the readings from the analog input
float readings2[numReadings];      // the readings from the analog input
float readings3[numReadings];      // the readings from the analog input

int readIndex = 0;              // the index of the current reading
int total1 = 0;    
int total2 = 0;  
int total3 = 0;
int average1 = 0;
int average2 = 0;
int average3 = 0; 


void setup() {
  Serial.begin(9600); // Open serial monitor at 115200 baud to see ping results. 
  
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings1[thisReading] = 0;
  }
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings2[thisReading] = 0;
  }
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings3[thisReading] = 0;
  }
}

void pingSweep(float *ret_arr) {
  
  unsigned int uS_1 = sonar1.ping();
  delay(30);
  //unsigned int uS_2 = sonar2.ping();
  //delay(40);
  unsigned int uS_3 = sonar3.ping();
  delay(30);

  ret_arr[0] = uS_1/US_ROUNDTRIP_CM;
  //ret_arr[1] = uS_2/US_ROUNDTRIP_CM;
  ret_arr[2] = uS_3/US_ROUNDTRIP_CM;

}

void runPing(float *data_arr, float seconds) {

  double elapsed_time = 0;
  double time_taken = 0;
  while (seconds > elapsed_time) {
    clock_t start_t, end_t;
    start_t = clock();

    //ping sweep will go here

    end_t = clock();
    time_taken = (double)(end_t - start_t)/CLOCKS_PER_SEC;
  }
}

void loop() {
  float data_arr[3] = {0};
  pingSweep(data_arr);
  float sensor1 = data_arr[0];
  //float sensor2 = data_arr[1];
  float sensor3 = data_arr[2];

  total1 = total1 - readings1[readIndex];
  //total2 = total2 - readings2[readIndex];
  total3 = total3 - readings3[readIndex];
  
  readings1[readIndex] = data_arr[0];
  //readings2[readIndex] = data_arr[1];
  readings3[readIndex] = data_arr[2];

  total1 = total1 + readings1[readIndex];
  //total2 = total2 + readings2[readIndex];
  total3 = total3 + readings3[readIndex];
  
  readIndex = readIndex + 1;

  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
  }

  // calculate the average:
  average1 = total1 / numReadings;
  //average2 = total2 / numReadings;
  average3 = total3 / numReadings;

  Serial.print(average1);
  Serial.print("\t");
  Serial.print(average2);
  Serial.print("\t");
  Serial.print(average3);
  Serial.println("\t");
 
}
