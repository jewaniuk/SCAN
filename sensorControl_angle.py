# Import Python Libraries/Packages
import RPi.GPIO as GPIO
import time
import json
from datetime import date

# Define the speed of sound in air at ~room temperature
vSound = 34400 # cm/s

# Define the delay between pings in adjacent sensors
delay = 0.04 # s

# Define the number of ultrasonic sensors in the array
numSensors = 2

# Use GPI0 ## to Define PINs
GPIO.setmode(GPIO.BCM)

# RPi PIN Setup (Straight Down)
PIN_TRIG_1 = 23
GPIO.setup(PIN_TRIG_1, GPIO.OUT)
GPIO.output(PIN_TRIG_1, False)
PIN_ECHO_1 = 24
GPIO.setup(PIN_ECHO_1, GPIO.IN)

PIN_TRIG_2 = 17
GPIO.setup(PIN_TRIG_2, GPIO.OUT)
GPIO.output(PIN_TRIG_2, False)
PIN_ECHO_2 = 27
GPIO.setup(PIN_ECHO_2, GPIO.IN)

# RPi PIN Setup (Angled)
PIN_TRIG_3 = 5
GPIO.setup(PIN_TRIG_3, GPIO.OUT)
GPIO.output(PIN_TRIG_3, False)
PIN_ECHO_3 = 6
GPIO.setup(PIN_ECHO_3, GPIO.IN)

PIN_TRIG_4 = 22
GPIO.setup(PIN_TRIG_4, GPIO.OUT)
GPIO.output(PIN_TRIG_4, False)
PIN_ECHO_4 = 6
GPIO.setup(PIN_ECHO_4, GPIO.IN)

# Conduct a single measurement of one ultrasonic sensor specified by its trigger and echo PINs
def ping(trig, echo):
    # Set desired trigger HIGH for 0.01 ms (this is the required time by the HC-SR04 datasheet)
    GPIO.output(trig, True)
    time.sleep(0.00001) 
    GPIO.output(trig, False)

    # Wait until the desired echo is HIGH to start the timer
    while GPIO.input(echo) == 0:
        pulseStart = time.time()

    # Wait until the desired echo is LOW to end the timer
    while GPIO.input(echo) == 1:
        pulseEnd = time.time()
    
    # Compute the pulse duration followed by the distance
    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * vSound / 2.0

    return pulseEnd, distance

# Conduct measurements by all ultrasonic sensors consecutively and use delay to avoid crosstalk
def arrayScan(trigs, echos):
    # Ping the array of sensors consecutively with the desired delay in between
    times = []
    distances = []
    for i in range(numSensors):
        # Store distance measurements and their respective times from each ping in lists
        pulseTime, pulseDistance = ping(trigs[i], echos[i])
        times.append(pulseTime)
        distances.append(pulseDistance)
        time.sleep(delay)

    return times, distances


def conductTest(maxTime):
    trigs_str = [PIN_TRIG_1, PIN_TRIG_2]
    echos_str = [PIN_ECHO_1, PIN_ECHO_2]
    trigs_ang = [PIN_TRIG_3, PIN_TRIG_4]
    echos_ang = [PIN_ECHO_3, PIN_ECHO_4]

    # Record initial time for the test
    testStart = time.time()

    # Ping the array of ultrasonic sensors continuously (with set delays) until the maximum test time is reached
    times = [[] for i in range(numSensors)]
    distances = [[] for i in range(numSensors)]
    while (time.time() - testStart) < maxTime:
        scanTimes, scanDistances = arrayScan(trigs, echos)
        # Store the data for each sensor in seperate lists within lists of lists
        for i in range(numSensors):
            times[i].append(scanTimes[i] - testStart)
            distances[i].append(scanDistances[i])

    # Convert the lists of lists to lists of tuples with data points (time, distance) for each sensor
    results = {}
    for i in range(numSensors):
        # Store lists of tuples by sensor number in a dictionary for the output JSON file
        results[i + 1].append(zip(times[i], distances[i]))

    # Write all results to an output JSON file
    now = date.now()
    filename = "Results/" + now.strftime("%b-%d-%Y_%H:%M:%S") + "_angled.json"
    with open(filename, 'w') as file:
        json.dump(results, file)