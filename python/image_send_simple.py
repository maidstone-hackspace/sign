from PIL import Image
import numpy as np
import sys
import serial
import struct
import time

#save as a greyscale png 8x8 pixels, test image made in GIMP
#dsrdtr setting this true will reset the arduino

ser = serial.Serial(
    port='/dev/ttyACM1',
    baudrate=115200,
    timeout=0,
    rtscts=True, dsrdtr=True
)

print ser.isOpen()
time.sleep(5)

#convert the array to an array with the strings concatenated
def drawImage(im):
    result = []
    for row in im:
        result.append(''.join([str(num) for num in row]))
    return result

def clear(display=0):
    ser.write(chr(display) + chr(0) + chr(0))
    s = ser.read(ser.inWaiting())

def drawList(data, display=0):
    for row in range(0, 8):
        offset = int(data[row], 2)
        ser.write(chr(display) + chr(row + 1) + chr(offset))
        s = ser.read(ser.inWaiting())

def loadImage(filename):
    im = Image.open(filename)
    im_array = np.array(im)
    im_array[im_array < 128] = 1 # any value in the array greater than 128 change it to the value 1
    im_array[im_array > 128] = 0 # any value in the array greater than 128 change it to the value 1
    return drawImage(im_array)

invader1 = loadImage('invader1.png')
invader2 = loadImage('invader2.png')

print invader1
print invader2

while True:
    #~ clear(0)
    #~ clear(1)
    drawList(invader1, 0)
    drawList(invader2, 1)
    time.sleep(1)

    #~ for disp in range(0, 2):
    #~ clear(0)
    #~ clear(1)
    #~ drawList(invader2, 0)
    #~ drawList(invader1, 1)
    #~ time.sleep(1)
    #~ 

ser.close()
