from PIL import Image
import numpy as np
import sys
import serial
import struct
import time

#save as a greyscale png 8x8 pixels, test image made in GIMP
#dsrdtr setting this true will reset the arduino

ser = serial.Serial(
    port='/dev/ttyACM0',
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
    #~ for column in row:
        #~ print p
            #~ offset = row
            #~ ser.write(chr(display) + chr(row + 1) + chr(offset))

def drawList(data, display=0):
    for row in range(0, 8):
        offset = int(data[row], 2)
        ser.write(chr(display) + chr(row + 1) + chr(offset))
        s = ser.read(ser.inWaiting())

im = Image.open("grid.png")
im_array = np.array(im)
im_array[im_array > 128] = 1 # any value in the array greater than 128 change it to the value 1
im_formatted = drawImage(im_array)


while True:
    for disp in range(0, 2):
        drawList(drawImage(im_array), 0)
        time.sleep(1)

        # flip the array
        drawList(drawImage(im_array.T), 0)
        time.sleep(1)

ser.close()
