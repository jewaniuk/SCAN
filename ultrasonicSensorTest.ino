// include the library code
#include "NewPing.h"
#include <stdio.h>
#include <time.h>


#define TRIGGER_PIN_1  3  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN_1     2  // Arduino pin tied to echo pin on the ultrasonic sensor.

#define TRIGGER_PIN_2  5  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN_2     4  // Arduino pin tied to echo pin on the ultrasonic sensor.

#define MAX_DISTANCE 250 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar1(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup() {
  Serial.begin(9600); // Open serial monitor at 115200 baud to see ping results. 
}

void pingSweep(float *ret_arr) {
  
  unsigned int uS_1 = sonar1.ping();
  delay(30);
  unsigned int uS_2 = sonar2.ping();

  ret_arr[0] = uS_1/US_ROUNDTRIP_CM;
  ret_arr[1] = uS_2/US_ROUNDTRIP_CM;

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
  float data_arr[2] = {0};
  pingSweep(data_arr);
  float sensor1 = data_arr[0];
  float sensor2 = data_arr[1];

  Serial.print(sensor1);
  Serial.print("\t");
  Serial.print(sensor2);
  Serial.print("\t");
 
}
