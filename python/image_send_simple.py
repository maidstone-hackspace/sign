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
    print 'return='
    print s

def largeScroll(data, xoffset, yoffset=0, display=1, left=True):
    # draw each column send a byte of data to light up all 8 leds
    for column_step in range(0, 8): 
        print '--scroll--'
        print xoffset
        # fetch the relevant byte fof data to send
        data_byte = data_wrap(data, xoffset, column_step, left)
        
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
    for column_step in range(0, 8):
        drawColumn(
            column=column_step + 1, 
            data=data[column_step], 
            display=display)

def loadImage(filename):
    """takes a greyscale png file"""
    im = Image.open(filename)
    im_array = np.array(im.convert('L'))

    im_array[im_array < 128] = 1 # any value in the array greater than 128 change it to the value 1
    im_array[im_array > 128] = 0 # any value in the array greater than 128 change it to the value 1
    print im_array
    return formatImage(im_array.T)

invader1 = loadImage('invader1.png')
invader2 = loadImage('invader2.png')
mhackspace = loadImage('mhackspace.png')
mhackspace_multiline = loadImage('mhackspace_multiline.png')
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
            data_byte = ''.join(
                [data[data_position][char_pos % len(data)] for char_pos in range(0, 8)])
        else : 
            data_byte = ''.join(
                [data[data_position][char_pos % len(data)] for char_pos in range(7, -1, -1)])
    return data_byte


image_width = len(mhackspace_multiline)
image_height = len(mhackspace_multiline[0])
print image_width
print image_height
#~ sys.exit(1)
matrix_offsets = []

# example image / animation
#~ while True:
for i in range(0, 6):
    print 'test'
    #~ drawImage(invader1, 1)
    #~ time.sleep(0.5)
    #~ drawImage(invader2, 1)
    #~ time.sleep(0.5)
    drawImage(invader1, 5)
    #~ time.sleep(0.5)
    #~ drawImage(invader2, 5)
    #~ time.sleep(0.5)
    sys.exit()

matrix_one = offsetter(32, image_width)
matrix_two = offsetter(24, image_width)
matrix_three = offsetter(16, image_width)
matrix_four = offsetter(8, image_width)
matrix_five = offsetter(0, image_width)

# display one is the last one in the chain
while True:
    #~ largeScroll(next(matrix_one), invader1, 1)
    #~ largeScroll(next(matrix_two), invader1, 2)
    #~ largeScroll(next(matrix_three), invader1, 3)
    
    pos1 = next(matrix_one)
    pos2 = next(matrix_two)
    pos3 = next(matrix_three)
    pos4 = next(matrix_four)
    pos5 = next(matrix_five)
    largeScroll(data=mhackspace, xoffset=pos1, display=1, left=False)
    largeScroll(data=mhackspace, xoffset=pos2, display=2, left=False)
    largeScroll(data=mhackspace, xoffset=pos3, display=3, left=False)
    largeScroll(data=mhackspace, xoffset=pos4, display=4, left=False)
    largeScroll(data=mhackspace, xoffset=pos5, display=5, left=False)
    #~ largeScroll(data=mhackspace, xoffset=pos3, display=4, left=False)
    #~ largeScroll(data=mhackspace, xoffset=pos3, display=5, left=False)
    
    #largeScroll(pos2, mhackspace, 2, False)
    #largeScroll(pos1, mhackspace, 3, False)

    #~ largeScroll(data=mhackspace_multiline, xoffset=pos3, yoffset=1, display=1, left=False)

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
