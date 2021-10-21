# Import Python Libraries & Modules
import numpy as np
import json
import matplotlib as mpl
import matplotlib.pyplot as plt

# Adjust Matplotlib Settings
mpl.rc('text', usetex=True)
mpl.rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Sans Serif']})
mpl.rc('mathtext', fontset='stixsans')
mpl.rc('text.latex', preamble=r'\usepackage{sansmathfonts}\renewcommand{\familydefault}{\sfdefault}\DeclareFontSeriesDefault[sf]{bf}{bx}')

# Define the number of ultrasonic sensors in the array
numSensors = 2

filename = "Results/Oct-21-2021_15:00:00.json"
with open(filename, 'r') as file:
    results = json.load(file)
file.close()

colours = ['#93032E', '#6184D8', '#F0803C', '#28AFB0', '#EDF060']
for i in range(numSensors):
    sensorResults = np.array(results[str(i+1)])
    times, distances = sensorResults.T

    label = "Sensor " + str(i + 1)
    plt.plot(times, distances, c=colours[i], label=label)

plt.xlabel("Time [s]")
plt.ylabel("Distance [cm]")
plt.legend()
plt.show()