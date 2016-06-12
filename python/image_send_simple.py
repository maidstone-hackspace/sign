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


def loopWidth():
    while True:
        for row in range(0, 8):
            yield row

#~ def chunk():
    

xpos = loopWidth()

#convert the array to an array with the strings concatenated
def formatImage(im):
    result = []
    for row in im:
        result.append(''.join([str(num) for num in row]))
    return result

def clear(display=1):
    ser.write(chr(display) + chr(0) + chr(0))
    s = ser.read(ser.inWaiting())

def drawColumn(column, data, display=1):
    print '--column--'
    print data
    print int(data, 2)
    ser.write(chr(display) + chr(column) + chr(int(data, 2)))
    s = ser.read(ser.inWaiting())
    print s

def largeScroll(offset, data, display=1):
    # draw each column send a byte of data to light up all 8 leds
    for column_step in range(0, 8): 
        print '--scroll--'
        print offset
        # fetch the relevant byte fof data to send
        data_byte = data_wrap(data, offset, column_step)
        
        drawColumn(
            column=column_step + 1, 
            data=data_byte, 
            display=display)

def drawScroll(data, display=1):
    for column_step in range(0, 8):
        row = next(xpos)
        drawColumn(
            column=column_step + 1, 
            data=data[row], 
            display=display)
    row = next(xpos)

def drawImage(data, display=1):
    for row in range(0, 8):
        drawColumn(
            column=row+1, 
            data=data[row], 
            display=display)

def loadImage(filename):
    im = Image.open(filename)
    print im.mode
    im_array = np.array(im.convert('L'))

    #~ print im_array
    #~ print im_array[0][0]
    #~ sys.exit()
    im_array[im_array < 128] = 1 # any value in the array greater than 128 change it to the value 1
    im_array[im_array > 128] = 0 # any value in the array greater than 128 change it to the value 1
    print im_array
    return formatImage(im_array.T)

invader1 = loadImage('mhackspace.png')
#~ invader2 = loadImage('invader2.png')
#~ print invader1


pos = 0

def offsetter(pos, width):
    """ loop max width, change start position"""
    while True:
        pos += 1
        if pos > width:
            pos = 0
        yield pos

def data_wrap(data, offset, column, left=True):
    """ when scrolling we want to fetch 8 bytes and offset, wrap when the data is at the end"""
    data_byte = '00000000'
    
    data_position = offset + column
    
    if data_position < len(data):
        if left is True:
            data_byte = ''
            data_byte = ''.join(
                [data[data_position][char_pos % len(data)] for char_pos in range(0, 8)])
    return data_byte


image_width = len(invader1)
print image_width
#~ sys.exit(1)
matrix_offsets = []

matrix_one = offsetter(0, image_width)
matrix_two = offsetter(8, image_width)
matrix_three = offsetter(16, image_width)

while True:
    #~ drawScroll(invader1, 1)
    #~ time.sleep(0.5)

    #~ drawScroll(invader2, 1)
    #~ time.sleep(0.5)

    #~ for disp in range(0, 2):
    #~ clear(0)
    #~ clear(1)
    #~ drawImage(invader2, 1)
    #~ time.sleep(0.5)
    
    #~ largeScroll(next(matrix_one), invader1, 1)
    #~ largeScroll(next(matrix_two), invader1, 2)
    #~ largeScroll(next(matrix_three), invader1, 3)
    
    pos1 = next(matrix_one)
    pos2 = next(matrix_two)
    pos3 = next(matrix_three)
    largeScroll(pos3, invader1, 1)
    largeScroll(pos2, invader1, 2)
    largeScroll(pos1, invader1, 3)

    #~ drawScroll(invader2, 1)
    #~ drawScroll(invader2, 2)
    #~ time.sleep(0.5)
    #~ drawImage(invader2, 3)
    time.sleep(0.2)
    #~ drawList(invader1, 2)
    #~ time.sleep(1)
    #~ print invader1
    #~ print invader2

ser.close()
