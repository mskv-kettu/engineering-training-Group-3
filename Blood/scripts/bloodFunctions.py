#import spidev
import time
import numpy as np
import matplotlib.pyplot as plt


########################################
#   Open, use and close SPI ADC
########################################

#spi = spidev.SpiDev()

def initSpiAdc():
    spi.open(0, 0)
    spi.max_speed_hz = 1600000
    print ("SPI for ADC have been initialized")

def deinitSpiAdc():
    spi.close()
    print ("SPI cleanup finished")

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1


########################################
#   Save and read data
########################################

def save(samples, start, finish):
    filename = 'blood-data {}.txt'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start)))

    with open(filename, "w") as outfile:
        outfile.write('- Blood Lab\n')
        outfile.write('- Date: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        outfile.write('- Duration: {:.2f} s\n\n'.format(finish - start))
        
        np.savetxt(outfile, np.array(samples).T, fmt='%d')

def read(filename):
    with open(filename) as f:
        lines = f.readlines()

    duration = float(lines[2].split()[2])
    samples = np.asarray(lines[4:], dtype=int)
    
    return samples, duration, len(samples)

########################################
#   Plot
########################################

colors = ["orange", "blue", "green", "red", "purple", "brown", "grey", "yellow", "cyan"]
plotDir = "plots/"

def Plot(data, plotSave, plotName, xname, yname, lineName, lineStyle, mark):
    fig = plt.figure(figsize=(10, 6), dpi=400)
    
    # Grid
    ax = plt.axes() 
    ax.minorticks_on()
    ax.grid(which='major', linewidth = 1)
    ax.grid(which='minor',linestyle = '--')
    
    #Plot building
    i = 0
    for plot in data:
        plt.plot(plot[0], plot[1], linestyle = lineStyle[i], color = colors[i], marker = mark[i], label='{}'.format(lineName[i]))
        i+=1
    plt.title(plotName)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.legend()
    plt.savefig( plotDir + plotSave + ".png")