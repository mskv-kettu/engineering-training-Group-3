from matplotlib.pyplot import vlines
import numpy as np
from jetFunctions import read
from jetFunctions import Plot
from pathlib import Path


########################################
#   Calibration
########################################

i = 0
points = []
dataDir = "data/calibration/"
for file in Path(dataDir).iterdir():
    data, steps, dataLen = read(file)
    points.append(np.mean(data))
# Preasure
p1 = 70
p0 = 0

pressure = [p0, p1]
kPress = (p1 - p0) / (points[1] - points[0]) # Коэф Давления
sValue = points[0] * kPress

plotSave = "pressure-calibration"
plotName = "Калибровочный график\nзависимости показаний АЦП от давления"
xname = "Давление [Па]"
yname = "Отсчёты АЦП"
lineName = ["P = {} * N - {} [Па]".format("%0.3f" % kPress, "%0.2f" % sValue)]
color = ["orange"]
mark = True
data = [[pressure, points]]
Plot(data, plotSave, plotName, xname, yname, lineName, color, mark)

Steps = [0, 880]
sm = [0, 4.5]
kStep = (sm[1] - sm[0]) / (Steps[1] - Steps[0]) # Коэф Перемещения

plotSave = "distance-calibration"
plotName = "Калибровочный график\nзависимости перемещения трубки Пито от шага двигателя"
xname = "Перемещение трубки Пито [см]"
yname = "Количество шагов"
lineName = ["X = {0:.1e} * step [м]".format(kStep / 100)]
color = ["orange"]
mark = True
data = [[sm, Steps]]
Plot(data, plotSave, plotName, xname, yname, lineName, color, mark)
kStep = kStep * 10 # В мм


########################################
#   Proscessing every file
########################################

from math import sqrt
from math import pi
dataDir = "data/"
data = []
color = ["blue", "orange", "green", "red", "purple", "brown", "pink", "grey", "yellow", "cyan", "0"]
plotName = "Скорость потока воздуха\nв сечении затопленной струи"
plotSave = "velocity-outgo"
lineName = []
mark = False
kInt = 2 * pi * 1.2 * kStep
for f in range(00, 101, 10):
    try:
        strF = str(f)
        if (f == 0):
             strF = "00"
        file = "data/"+ strF + " mm.txt"
        values, steps, dataLen = read(file)
        ur = [1]*len(values)
        r = np.arange(-dataLen/2, dataLen/2) * kStep # Здесь проблема
        velocities = [1] * len(values)

        for i in range(len(values)):
            dynPress = kPress*values[i]-sValue
            if (dynPress < 2.5):
                dynPress = 0
            velocities[i] = sqrt(2* abs(dynPress) / 1.2) # Формула для скорости
            ur[i] = velocities[i]* kInt * r[i] / 1000
        Q = 0
        for i in range (len(ur)):
            Q += abs(ur[i])
        Q = Q / 2
        plot = [r, velocities]
        data.append(plot)
        lineName.append("Q ({} мм) = {} [г/с]".format(strF, "%0.2f" % Q))
    except:
        continue
Plot(data, plotSave ,plotName, "Положение трубки Пито относительно центра струи [мм]", "Скорость воздуха [м/с]", lineName, color, False)