import time
import picamera
import picamera.array
import numpy as np
from PIL import Image

with picamera.PiCamera() as camera:
camera.resolution = (2560, 1440)
camera.start_preview()
time.sleep(1)
camera.capture("photoname.png")
im.save("photoname.png")