#import spidev
import time
#import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt

########################################
#   Open, use and close SPI ADC
########################################

#spi = spidev.SpiDev()

def initSpiAdc():
    spi.open(0, 0)
    spi.max_speed_hz = 1600000
    print ("SPI for ADC has been initialized")

def deinitSpiAdc():
    spi.close()
    print ("SPI cleanup finished")

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

def getMeanAdc(samplesInMeasure):
    sum = 0
    for i in range(samplesInMeasure):
        sum += getAdc()
    
    return int(sum / samplesInMeasure)


########################################
#   Setup and use GPIO for step motor
########################################

directionPin = 27
enablePin = 22
stepPin = 17

def initStepMotorGpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([directionPin, enablePin, stepPin], GPIO.OUT)
    print ("GPIO for step motor have been initialized")

def deinitStepMotorGpio():
    GPIO.output([directionPin, enablePin, stepPin], 0)
    GPIO.cleanup()
    print ("GPIO cleanup finished")

def step():
    GPIO.output(stepPin, 0)
    time.sleep(0.005)
    GPIO.output(stepPin, 1)
    time.sleep(0.005)
    
def stepForward(n):
    GPIO.output(directionPin, 1)
    GPIO.output(enablePin, 1)

    for i in range(n):
        step()

    GPIO.output(enablePin, 0)

def stepBackward(n):
    GPIO.output(directionPin, 0)
    GPIO.output(enablePin, 1)

    for i in range(n):
        step()

    GPIO.output(enablePin, 0)


########################################
#   Save and read data
########################################

def save(measures, motorSteps):
    filename = 'jet-data {}.txt'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    with open(filename, "w") as outfile:
        outfile.write('- Jet Lab\n')
        outfile.write('- Date: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        outfile.write('- Step: {} motor steps\n'.format(motorSteps))
        
        np.savetxt(outfile, np.array(measures).T, fmt='%d')

def read(filename):
    with open(filename) as f:
        lines = f.readlines()

    steps = int(lines[2].split()[2])
    measures = np.asarray(lines[4:], dtype=int)

    return measures, steps, len(measures)

########################################
#   Plot
########################################

def Plot(data, plotSave, plotName, xname, yname, lineName, color, mark):
    fig = plt.figure(figsize=(10, 6), dpi=200)
    # Grid
    ax = plt.axes() 
    ax.minorticks_on()
    ax.grid(which='major', linewidth = 1)
    ax.grid(which='minor',linestyle = '--')
    #Plot building
    i = 0
    for plot in data:
        if (mark):
            plt.plot(plot[0], plot[1], color = color[i], label='{}'.format(lineName[i]))
        else:
            plt.plot(plot[0], plot[1], color = color[i], label='{}'.format(lineName[i]))
        i+=1
    plt.title(plotName)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.legend()
    plt.savefig( "plots/" + plotSave + ".png")
