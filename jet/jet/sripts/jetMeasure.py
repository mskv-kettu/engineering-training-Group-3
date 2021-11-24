# Experiment

import jetFunctions as jf

maxShift = 300
maxShift = int(input("Enter Shift (defult = 300): "))
Steps = int(input("Enter current steps: "))
try:
    shift = 0

    jf.initStepMotorGpio()
    jf.initSpiAdc()

    shift = shift-maxShift
    jf.stepBackward(maxShift)
    
    data = [1] * (2*maxShift)
    for i in range(2*maxShift):
        data[i] = jf.getAdc()
        shift += 1
        jf.stepForward(1)
    
    shift -= maxShift
    jf.stepBackward(maxShift)
    jf.save(data, Steps)
    

finally:
    jf.deinitStepMotorGpio()
    jf.deinitSpiAdc()
