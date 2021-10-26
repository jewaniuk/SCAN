# Import Python Libraries/Packages
import RPi.GPIO as GPIO
import time
import json
from datetime import datetime as date

# Define the speed of sound in air at ~room temperature
vSound = 34400 # cm/s

# Define the delay between pings in adjacent sensors
delay = 0.04 # s

# Define the number of ultrasonic sensors in the array
numSensors = 2

# Use GPI0 ## to Define PINs
GPIO.setmode(GPIO.BCM)

# RPi PIN Setup
PIN_TRIG_1 = 21
GPIO.setup(PIN_TRIG_1, GPIO.OUT)
GPIO.output(PIN_TRIG_1, False)
PIN_ECHO_1 = 20
GPIO.setup(PIN_ECHO_1, GPIO.IN)

PIN_TRIG_2 = 18
GPIO.setup(PIN_TRIG_2, GPIO.OUT)
GPIO.output(PIN_TRIG_2, False)
PIN_ECHO_2 = 24
GPIO.setup(PIN_ECHO_2, GPIO.IN)

# Conduct a single measurement of one ultrasonic sensor specified by its trigger and echo PINs
def ping(trig, echo):
    # Set desired trigger HIGH for 0.01 ms (this is the required time by the HC-SR04 datasheet)
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001) 
    GPIO.output(trig, GPIO.LOW)
    trigDone = time.time()

    # Wait until the desired echo is HIGH to start the timer
    #while not GPIO.input(echo):
        #pulseStart = time.time()
        #print("ECHO IS LOW")

    # Wait until the desired echo is LOW to end the timer
    pulseStart = trigDone
    checkON = False
    while (time.time() - trigDone) < 0.031:
        if (not GPIO.input(echo)) and (not checkON):
            pulseStart = time.time()
        else:
            pulseEnd = time.time()
            checkON = True
        print("ECHO IS HIGH")
    
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
        try:
            pulseTime, pulseDistance = ping(trigs[i], echos[i])
        except:
            pulseTime, pulseDistance = (time.time(), 4)
            print("SHAQ WALKED IN")
        times.append(pulseTime)
        distances.append(pulseDistance)
        time.sleep(delay)
    time.sleep(delay)

    return times, distances


def conductTest(maxTime):
    trigs = [PIN_TRIG_1, PIN_TRIG_2]
    echos = [PIN_ECHO_1, PIN_ECHO_2]

    # Record initial time for the test
    testStart = time.time()

    # Ping the array of ultrasonic sensors continuously (with set delays) until the maximum test time is reached
    times = [[] for i in range(numSensors)]
    distances = [[] for i in range(numSensors)]
    while (time.time() - testStart) < maxTime:
        scanTimes, scanDistances = arrayScan(trigs, echos)
        print("Completed Array Scan", time.time() - testStart)
        # Store the data for each sensor in seperate lists within lists of lists
        for i in range(numSensors):
            times[i].append(scanTimes[i] - testStart)
            distances[i].append(scanDistances[i])

    # Convert the lists of lists to lists of tuples with data points (time, distance) for each sensor
    results = {}
    for i in range(numSensors):
        # Store lists of tuples by sensor number in a dictionary for the output JSON file
        results[i + 1] = []
        results[i + 1].append(list(zip(times[i], distances[i])))

    # Write all results to an output JSON file
    now = date.now()
    filename = "/home/pi/Documents/SCAN/Results/" + now.strftime("%b-%d-%Y_%H:%M:%S") + ".json"
    with open(filename, 'w') as file:
        json.dump(results, file)

maxTime = 10 # s
conductTest(maxTime)
