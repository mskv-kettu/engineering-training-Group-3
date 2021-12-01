import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time
import spidev
import bloodFunctionsr as bf

value_list = []

def adc():   #считывание данных с АЦП SPI
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

def calibration(mm):     #калибровка на данную величину давления, запись в txt
    print("Калибровка " + str(mm))
    begin = time.time()
    value_calibration = []
    while time.time() - begin < 10:
        value_calibration.append(adc())
    duration_calibration = time.time()
#    value_calibration_str = [str(item) for item in value_calibration]
    bf.save(value_calibration, begin, duration_calibration)
    print("Калибровка завершена\n")

def start_calibration():    #функция, которая запускает полную калибровку
    print("Проводится калибровка! \n")
    input("Выставьте давление 160\n")
    calibration(160)
    input("Выставьте давление 120\n")
    calibration(120)
    input("Выставьте давление 80\n")
    calibration(80)
    input("Выставьте давление 40\n")
    calibration(40)

try:
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1600000

    start_calibration()    #один раз сделать, потом закомментировать

    input("\nГотово для начала эксперимента")   #само измерение. Вводим символ и жмем enter, когда готовы.
    begin = time.time()                         #Строго 1 минута выполнения
    print("Начало измерений")
    while (time.time() - begin < 60):
        value_list.append(adc())

finally:
    print("Конец измерений")

    duration = time.time()
    print("Duration = {:.2f} sec".format(duration))
    print("Counts = {}".format(len(value_list)))

    value_list_str = [str(item) for item in value_list]

    bf.save(value_list, begin, duration)

    plt.plot(value_list)
    plt.show()

    GPIO.cleanup()
    spi.close()