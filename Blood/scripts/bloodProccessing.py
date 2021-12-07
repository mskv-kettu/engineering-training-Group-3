import numpy as np
from bloodFunctions import read
from bloodFunctions import Plot
from pathlib import Path


########################################
#   Calibration
########################################

dataDir = "data/calibration/"

ADC = []
pressure = []
for file in Path(dataDir).iterdir():
    samples, duration, samplesLen = read(file)
    ADC.append(np.mean(samples))
    pressure.append(int( str(file)[len(dataDir):].split(" ")[0] ))

# factor by polynom
presFactors =  np.polyfit(ADC, pressure, 1)
plotData = [[np.polyval(presFactors, ADC), ADC], [pressure, ADC]]

# Calibration Graph
plotName = "Калибровочный график зависимости\nпоказаний АЦП от давления"
plotSave = "pressure-calibration"
xAxisName = "Давление [мм рт. ст.]"
yAxisName = "Отсчёты АЦП"
lineName = ["P = {} * N + ({}) [мм рт. ст.]".format("%0.3f" % presFactors[0], "%0.2f" % presFactors[1]), "Измерения"]
lineStyle = ["-", "None"]
mark = [",", "*"]
Plot(plotData, plotSave, plotName, xAxisName, yAxisName, lineName, lineStyle, mark)

import matplotlib.pyplot as plt

########################################
#   Fitness
########################################

dataDir = "data/"

xAxisName = "Время [с]"
file = dataDir + "fitness.txt"
samples, duration, samplesLen = read(file)
pressure = np.array(samples)
pressure = np.polyval(presFactors, pressure)
time = np.arange(samplesLen) * (duration/samplesLen)

#----------------- Pulse -----------------
for i in range (len(pressure)):
    if abs(pressure[i] - 140) < 0.05:
        systole = i
    if abs(pressure[i] - 110) < 0.05:
        dyastole = i
    
pPres =[]
pTime = []
systoleN = systole + round(5 * samplesLen/duration)
poly = np.polyfit([time[systole], time[systoleN]], [pressure[systole], pressure[systoleN]], 1)

for i in range(systole, systoleN):
    pTime.append(time[i])
    pPres.append(pressure[i] - np.polyval(poly, time[i]))

poly = np.polyfit

yAxisName = "Давление [мм рт. ст.]"
data = [pTime, pPres]
plotSave = "fitness-pulse.png"
plotName = "Пульс\nпосле физической нагрузки"
lineName = "Пульс = 108"

fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
plt.plot(data[0], data[1], color = "orange", label='{}'.format(lineName))

plt.title(plotName)
plt.xlabel(xAxisName)
plt.ylabel(yAxisName)

plt.legend()
plt.savefig( "plots/" + plotSave)

#----------------- Pressure -----------------

time = np.arange(samplesLen) * (duration/samplesLen)
yAxisName = "Давление [мм рт. ст.]"
data = [time, pressure]
plotSave = "fitness-pressure.png"
plotName = "Артериальное давление\nпосле физической нагрузки"
lineName = "Давление 140/110"

fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
#Plot building
plt.xlim(0, 40)
plt.ylim(100, 170)
plt.plot(data[0], data[1], color = "orange", label='{}'.format(lineName))
plt.plot(time[systole], pressure[systole], color = "red", marker = "*")
plt.plot(time[dyastole], pressure[dyastole], color = "red", marker = "*")
ax.annotate("systole", (time[systole], pressure[systole]))
ax.annotate("dyastole", (time[dyastole], pressure[dyastole]))

plt.title(plotName)
plt.xlabel(xAxisName)
plt.ylabel(yAxisName)

plt.legend()
plt.savefig( "plots/" + plotSave)


########################################
#   Rest
########################################

xAxisName = "Время [с]"
file = dataDir + "rest.txt"
samples, duration, samplesLen = read(file)
pressure = np.array(samples)
pressure = np.polyval(presFactors, pressure)
time = np.arange(samplesLen) * (duration/samplesLen)

#----------------- Pulse -----------------

for i in range (len(pressure)):
    if abs(pressure[i] - 108) < 0.05:
        systole = i
    if abs(pressure[i] - 80) < 0.05:
        dyastole = i

pPres =[]
pTime = []
systoleN = systole + round(5 * samplesLen/duration)
poly = np.polyfit([time[systole], time[systoleN]], [pressure[systole], pressure[systoleN]], 1)

for i in range(systole, systoleN):
    pTime.append(time[i])
    pPres.append(pressure[i] - np.polyval(poly, time[i]))

poly = np.polyfit

yAxisName = "Давление [мм рт. ст.]"
data = [pTime, pPres]
plotSave = "rest-pulse.png"
plotName = "Пульс\nдо физической нагрузки"
lineName = "Пульс = 84"

fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
plt.plot(data[0], data[1], color = "orange", label='{}'.format(lineName))

plt.title(plotName)
plt.xlabel(xAxisName)
plt.ylabel(yAxisName)

plt.legend()
plt.savefig( "plots/" + plotSave)
#----------------- Pressure -----------------

time = np.arange(samplesLen) * (duration/samplesLen)
yAxisName = "Давление [мм рт. ст.]"
data = [time, pressure]
plotSave = "rest-pressure.png"
plotName = "Артериальное давление\nдо физической нагрузки"
lineName = "Давление 108/"

fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
#Plot building
plt.xlim(20, 60)
plt.ylim(80, 130)
plt.plot(data[0], data[1], color = "orange", label='{}'.format(lineName))
plt.plot(time[systole], pressure[systole], color = "red", marker = "*")
plt.plot(time[dyastole], pressure[dyastole], color = "red", marker = "*")
ax.annotate("systole", (time[systole], pressure[systole]))
ax.annotate("dyastole", (time[dyastole], pressure[dyastole]))
plt.title(plotName)
plt.xlabel(xAxisName)
plt.ylabel(yAxisName)

plt.legend()
plt.savefig( "plots/" + plotSave)

print ("done")