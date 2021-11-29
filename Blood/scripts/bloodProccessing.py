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
deltaPres = [1] * (samplesLen - 21)
sval = pressure[0]
aftertop = False
for i in range(samplesLen-21):
    if pressure[i+20] - pressure[i] > 0 and aftertop:
        sval = pressure[i]
        aftertop = False
    if pressure[i+20] - pressure[i] < 0:
        aftertop = True
    deltaPres[i] = pressure[i] - sval
time = np.arange(len(deltaPres)) * (duration/len(deltaPres))
pulse = 0

# (разрешающая способность пульса) Эмпирический коэффициент
dT = round(samplesLen / duration * 0.11)


for i in range(0,len(deltaPres) - 1,  dT):
    if deltaPres[i] * deltaPres[i+1] <= 0:
        pulse= pulse + 1

lineName = "Пульс — {} [уд/мин]".format(pulse)
fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
#Plot building

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
deltaPres = [1] * (samplesLen - 21)
sval = pressure[0]
aftertop = False
for i in range(samplesLen-21):
    if pressure[i+20] - pressure[i] > 0 and aftertop:
        sval = pressure[i]
        aftertop = False
    if pressure[i+20] - pressure[i] < 0:
        aftertop = True
    deltaPres[i] = pressure[i] - sval
time = np.arange(len(deltaPres)) * (duration/len(deltaPres))
pulse = 0

# (разрешающая способность пульса) Эмпирический коэффициент
dT = round(samplesLen / duration * 0.11)


for i in range(0,len(deltaPres) - 1,  dT):
    if deltaPres[i] * deltaPres[i+1] <= 0:
        pulse= pulse + 1

lineName = "Пульс — {} [уд/мин]".format(pulse)
fig = plt.figure(figsize=(10, 6), dpi=200)  
# Grid
ax = plt.axes() 
ax.minorticks_on()
ax.grid(which='major', linewidth = 1)
ax.grid(which='minor',linestyle = '--')
#Plot building

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
plt.title(plotName)
plt.xlabel(xAxisName)
plt.ylabel(yAxisName)

plt.legend()
plt.savefig( "plots/" + plotSave)