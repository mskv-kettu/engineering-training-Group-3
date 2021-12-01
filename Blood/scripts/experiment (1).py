import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time
import spidev

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
    duration_calibration = time.time() - begin
    value_calibration_str = [str(item) for item in value_calibration]
    with open(str(mm) + " mmHg.txt", "w") as mmHg:
        mmHg.write('- Blood Lab\n\n')
        mmHg.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        mmHg.write('- Experiment duration = {:.2f} s\n'.format(duration_calibration))
        mmHg.write('- Sampling period = {:.2f} mcs\n'.format(duration_calibration / len(value_calibration) * 1000000))
        mmHg.write('- Sampling frequency = {} Hz\n'.format(int(len(value_calibration) / duration_calibration)))
        mmHg.write('- Samples count = {}\n'.format(len(value_calibration)))
        mmHg.write("\n".join(value_calibration_str))
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

    duration = time.time() - begin
    print("Duration = {:.2f} sec".format(duration))
    print("Counts = {}".format(len(value_list)))

    value_list_str = [str(item) for item in value_list]

    with open("finalfitness.txt", "w") as data:
        data.write('- Blood Lab\n\n')
        data.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        data.write('- Experiment duration = {:.2f} s\n'.format(duration))
        data.write('- Sampling period = {:.2f} mcs\n'.format(duration / len(value_list) * 1000000))
        data.write('- Sampling frequency = {} Hz\n'.format(int(len(value_list) / duration)))
        data.write('- Samples count = {}\n'.format(len(value_list)))
        data.write("\n".join(value_list_str))

    plt.plot(value_list)
    plt.show()

    GPIO.cleanup()
    spi.close()