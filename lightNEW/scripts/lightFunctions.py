import numpy as np
import matplotlib.pyplot as plt
import imageio
from PIL import Image

def black_and_white(input_image_path, output_image_path):
   color_image = Image.open(input_image_path)
   bw = color_image.convert('L')
   bw.save(output_image_path)

PhStart = 1200
PHStop = 1360

# позаимствовано из примера и доделано
def readIntensity(dataDir, photoName, plotName, lamp, surface):
   tempDir = "temp/"
   monoPhotoName = tempDir + "/mono_" + photoName
   photoName = dataDir + photoName
   # преобразование в чб т.к. в примере усреднение по значениям для RGB, что странно
   black_and_white( photoName, monoPhotoName) 
   monoPhoto = imageio.imread(monoPhotoName)
   monoCut = np.flip(monoPhoto[425:1025, PhStart:PHStop].swapaxes(0, 1), axis = 1 )# (транспонирование) изображения
   intensity = np.mean(monoCut, axis=0) # усреднение яркости

   photo = imageio.imread(photoName)
   cut = np.flip(photo[425:1025, PhStart:PHStop, 0:3].swapaxes(0,1), axis = 1)
   fig = plt.figure(figsize=(10, 3), dpi=200)
   plt.plot(intensity, 'w', label='{} / {}'.format(lamp, surface))
   plt.imshow(cut, origin='lower')
   plt.title('Интенсивность отражённого излучения')
   plt.xlabel('Относительный номер пикселя')
   plt.ylabel('Яркость')
   plt.legend()
   plt.savefig(plotName)

   return intensity

def Plot(data, title, xlabel, xStart, valToPixel, ylabel,  plotName, lamp, surface):
   i = 0
   fig = plt.figure(figsize=(10, 6), dpi=200)
   ax = plt.axes()
   # Setting the background color + grid
   ax.set_facecolor("lightgrey")
   ax.minorticks_on()
   ax.grid(which='major', linewidth = 1)
   ax.grid(which='minor',linestyle = '-')

   for plot in data:
      plt.plot(plot, color = surface[i][0], label='{} / {}'.format(lamp[i], surface[i]))
      i+=1
   plt.title(title)
   plt.xlabel(xlabel)

   # black magic and illusions ЛУЧШЕ НЕ ПОЛУЧИЛОСЬ
   # ДОЛЖНЫ БЫТЬ polyfit и polyval, но разобраться пока не получилось
   pixel = np.arange(0,600, 100)
   x_labels = list()
   for i in range(len(pixel)):
      x_labels.append(round(xStart + valToPixel * pixel[i]))
   plt.xticks(pixel, x_labels)
 
   plt.ylabel(ylabel)
   plt.legend()
   plt.savefig(plotName)

def findColorMax(color, photoName):
   photo = imageio.imread(photoName)
   if color == "green":
      cut = np.flip(photo[425:1025, PhStart:PHStop, 1:2].swapaxes(0,1), axis = 1)
   if color == "blue":
      cut = np.flip(photo[425:1025, PhStart:PHStop, 2:3].swapaxes(0,1), axis = 1)
   intensity = np.mean(cut, axis=0)
   maxVal = 0
   pixel = -1
   for i in range(len(intensity)):
      if maxVal < intensity[i]:
         pixel = i
         maxVal = intensity[i]
   return pixel