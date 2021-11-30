import numpy as np
from bloodFunctions import read
from bloodFunctions import Plot
from pathlib import Path


########################################
#   Calibration
########################################

dataDir = "data example/calibration/"

ADC = []
pressure = []
for file in Path(dataDir).iterdir():
    samples, duration, samplesLen = read(file)
    ADC.append(np.mean(samples))
    pressure.append(int( str(file)[len(dataDir):].split(" ")[0] ))

plotData = [[pressure, ADC] , [pressure, ADC]]
# factor by polynom
presFactors =  np.polyfit(ADC, pressure, 1)
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

dataDir = "data example/"
xAxisName = "Время [с]"
file = dataDir + "fitness.txt"
samples, duration, samplesLen = read(file)
pressure = np.array(samples)
pressure = np.polyval(presFactors, pressure)
time = np.arange(samplesLen) * (duration/samplesLen)

#----------------- Pulse -----------------
plotSave = "fitness-pulse.png"
yAxisName = "Изменение давления в артерии [мм рт. ст.]"
plotName = "Пульс\nпосле физической нагрузки"
deltaPres = [1] * (samplesLen)
sval = pressure[0]
aftertop = False
systole = 0
# Чёрная магия
sigma = round (0.08 * samplesLen / duration)
left = np.arange(sigma)
right = np.arange(sigma)
p = []
for i in range(sigma,len(deltaPres)-sigma):
    k = 0
    for j in range(i, i-sigma, -1):
        left[k] = pressure[j]
        k+=1
    l = pressure[i] - np.mean(left)
    k = 0
    for j in range(i+1, i+sigma):
        right[k] = np.mean(right)
        k+=1
    r = pressure[i-sigma] - pressure[i]
    if r <= 0 and l >= 0:
        p.append(i)

pulse = 0
base = pressure[0]
CouldBeMax = False
for i in range(len(deltaPres)):
    if i in p:
        base = pressure[i]
    deltaPres[i] = pressure[i] - base
    if deltaPres[i] < -0.5:
        CouldBeMax = True
    if CouldBeMax and deltaPres[i] >= 0:
        pulse = pulse + 1
        CouldBeMax = False
        if pulse == 5:
            systole = i

time = np.arange(len(deltaPres)) * (duration/len(deltaPres))


lineName = "Пульс — {} [уд/мин]".format(pulse)
fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
#Plot building
plt.xlim(0, 20)
plt.ylim(-10, 1)
plt.plot(time, deltaPres, color = "orange", label='{}'.format(lineName))
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
lineName = "Давление"

fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
#Plot building
plt.xlim(0, 30)
plt.ylim(50, 190)
plt.plot(data[0], data[1], color = "orange", label='{}'.format(lineName))
plt.plot(time[systole], pressure[systole], color = "red", marker = "*")
plt.title(plotName)
plt.xlabel(xAxisName)
plt.ylabel(yAxisName)

plt.legend()
plt.savefig( "plots/" + plotSave)


########################################
#   Rest
########################################

dataDir = "data example/"
xAxisName = "Время [с]"
file = dataDir + "rest.txt"
samples, duration, samplesLen = read(file)
pressure = np.array(samples)
pressure = np.polyval(presFactors, pressure)
time = np.arange(samplesLen) * (duration/samplesLen)

#----------------- Pulse -----------------
plotSave = "rest-pulse.png"
yAxisName = "Изменение давления в артерии [мм рт. ст.]"
plotName = "Пульс\nдо физической нагрузки"
deltaPres = [1] * (samplesLen)
sval = pressure[0]
aftertop = False
# Чёрная магия 2
sigma = round (0.08 * samplesLen / duration)
left = np.arange(sigma)
right = np.arange(sigma)
p = []
for i in range(sigma,len(deltaPres)-sigma):
    k = 0
    for j in range(i, i-sigma, -1):
        left[k] = pressure[j]
        k+=1
    l = pressure[i] - np.mean(left)
    k = 0
    for j in range(i+1, i+sigma):
        right[k] = np.mean(right)
        k+=1
    r = pressure[i-sigma] - pressure[i]
    if r <= 0 and l >= 0:
        p.append(i)

pulse = 0
base = pressure[0]
CouldBeMax = False
for i in range(len(deltaPres)):
    if i in p:
        base = pressure[i]
    deltaPres[i] = pressure[i] - base
    if deltaPres[i] < -0.5:
        CouldBeMax = True
    if CouldBeMax and deltaPres[i] >= 0:
        pulse = pulse + 1
        CouldBeMax = False
        if pulse == 5:
            systole = i

lineName = "Пульс — {} [уд/мин]".format(pulse)
fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
#Plot building
plt.ylim(-10, 1)
plt.xlim(0, 20)
plt.plot(time, deltaPres, color = "orange", label='{}'.format(lineName))
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
lineName = "Давление"

fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
#Plot building
plt.xlim(0, 30)
plt.ylim(50, 190)
plt.plot(data[0], data[1], color = "orange", label='{}'.format(lineName))
plt.plot(time[systole], pressure[systole], color = "red", marker = "*")
plt.title(plotName)
plt.xlabel(xAxisName)
plt.ylabel(yAxisName)

plt.legend()
plt.savefig( "plots/" + plotSave)