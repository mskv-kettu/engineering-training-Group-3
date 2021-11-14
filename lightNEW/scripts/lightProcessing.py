import lightFunctions as lf
from pathlib import Path

numOfFiles = 7
fileNames = [numOfFiles, 2]
intensity = list()
intensity_lamp = list()
intensity_surface = list()
dataDir = "data/"
k = 0
for file in Path(dataDir).iterdir():
    str_file = str(file)
    str_file = str_file[str_file.index("data") + 5:]
    lamp = str_file[str_file.index('-') + 1: str_file.index('.')]
    if lamp == "mercury":
        continue
    surface = str_file[0:str_file.index('-')]
    im = lf.readIntensity(dataDir, str_file, "plots/" + str_file, lamp, surface)
    intensity.append(im)
    if lamp == "tungsten" and surface == "white":
        wh = k
    # lamp и surface, соответствующие intensity можно матрицей, но я боюсь, что ошибусь (можно лучше) 
    intensity_lamp.append(lamp)
    intensity_surface.append(surface)
    k+=1


mercury = lf.readIntensity("data/", "white-mercury.png", "plots/white-mercury.png", "mercury", "white")
xPixel = 600 # const, размер X оси
blueLen = 435.8328
greenLen = 546.0735
greenMax = lf.findColorMax("green", "data/white-mercury.png")
lenToPixel = (blueLen - greenLen) / (lf.findColorMax("blue", "data/white-mercury.png") - greenMax)
startLen = greenLen - lenToPixel * greenMax
endLen = startLen + lenToPixel * xPixel
lf.Plot(intensity, "Интенсивность отражённого излучения", "Длина волны [нм]", startLen, lenToPixel, "Яркость", "plots/intensities.png", intensity_lamp, intensity_surface)

# не правильно из-за 0/0
white = lf.readIntensity("data/", "white-tungsten.png", "plots/white-tungsten.png", "tungsten", "white")
for i in range (len(intensity)):
    for j in range (len(intensity[i])):
        if i == wh:
            intensity[i][j] = 1    
        else: # НЕ ЗНАЮ КАК СДЕЛАТЬ
            if white[j] < 0.1:
                white[j] += 0.1
            intensity[i][j] /= white[j]
        

lf.Plot(intensity, "Интенсивность отражённого излучения", "Длина волны [нм]", startLen, lenToPixel, "Альбедо", "plots/albedo.png", intensity_lamp, intensity_surface)

