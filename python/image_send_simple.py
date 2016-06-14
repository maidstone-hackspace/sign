from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
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

#~ def chunk():


#convert the array to an array with the strings concatenated
def formatImage(image_array):
    result = []
    for row in image_array:
        result.append(''.join([str(num) for num in row]))
    return result

def clear(display=1):
    ser.write(chr(display) + chr(0) + chr(0))
    s = ser.read(ser.inWaiting())

def drawColumn(column, data, display=1):
    ser.write(chr(display) + chr(column) + chr(int(data[0:8], 2)))
    s = ser.read(ser.inWaiting())

def largeScroll(data, xoffset, yoffset=0, display=1, left=True):
    # draw each column send a byte of data to light up all 8 leds
    for column_step in range(0, 8): 
        # fetch the relevant byte of data to send
        data_byte = data_wrap(data, xoffset, column_step, left)
        
        drawColumn(
            column=column_step + 1, 
            data=data_byte, 
            display=display)


def drawImage(data, offset=0, display=1):
    for column_step in range(0, 8):
        drawColumn(
            column=column_step + 1, 
            data=data[column_step + offset], 
            display=display)

def image_to_array(im):
    """file to load, must be a greyscale png
    Args:
      filename (string): filename of the image to load
    Returns:
      list: image data converted to a list"""
    im_array = np.array(im.convert('L'))

    im_array[im_array < 128] = 1 # any value in the array greater than 128 change it to the value 1
    im_array[im_array > 128] = 0 # any value in the array greater than 128 change it to the value 1
    print im_array
    return formatImage(im_array.T)

def loadImage(filename):
    """file to load, must be a greyscale png
    Args:
      filename (string): filename of the image to load
    Returns:
      list: image data converted to a list"""
    im = Image.open(filename)
    return image_to_array(im)

def loadText(text, bgcol=(0,0,0), fgcol=(255,255,255)):
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf",8)
    img = Image.new("L", (64, 8), bgcol)
    draw = ImageDraw.Draw(img)
    text_image = draw.text((0, 0), text, fgcol, font=font)
    img.save('test.png')
    return image_to_array(img)


mhackspace = loadImage('mhackspace.png')
mhackspace_multiline = loadImage('mhackspace_multiline.png')
#~ invader2 = loadImage('invader2.png')
#~ print invader1


pos = 0

def offsetter(start_pos, width, loop=True):
    """offset start, loop max width, loop forever or just stop incrementing at the end"""
    if loop is True:
        while True: # or pos < width:
            
            if start_pos > width:
                start_pos = 0
            yield pos
            start_pos += 1
    else:
        for start_pos in range(start_pos, width):
            yield start_pos
        while True:
            yield start_pos

def data_wrap(data, offset, column, left=True):
    """when scrolling we want to fetch 8 bytes and offset, wrap when the data is at the end

    Args:
      data (list): 2 dimensional list of the data to display
      offset (int): offset into the list
      column (int): column in the list
      left (vector): direction to shift
      
    Returns:
      data_byte: 8 byte string"""
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
matrix_offsets = []

mytext = loadText('HELLO')

# example rendering / font
def font_test(text_image):
    for i in range(0, 6):
        drawImage(mytext, 0, 1)
        drawImage(mytext, 8, 2)
        drawImage(mytext, 16, 3)
        drawImage(mytext, 24, 4)
        drawImage(mytext, 32, 5)
        time.sleep(0.5)


# example image / animation
def space_invader_animate(image_list):
    #loop a few times for the animation
    for i in range(0, 6):
        for image in image_list:
            drawImage(image, display=1)
            time.sleep(0.5)


def scroll_image_example(image_data):
    matrix_stepper = offsetter(start_pos=-8, width=image_width, loop=False)
    while True:
        d=1
        pos = next(matrix_stepper)
        for display in range(5, 0, -1):
            offset = pos + (display - 1) * 8
            largeScroll(data=image_data, xoffset=offset, display=d, left=False)
            d += 1

def scroll_pipes():
    matrix_stepper = offsetter(start_pos=-8, width=image_width, loop=False)
    while True:
        d=1
        pos = next(matrix_stepper)
        for display in range(5, 0, -1):
            offset = pos + (display - 1) * 8
            largeScroll(data=mhackspace, xoffset=offset, display=d, left=False)
            d += 1

invader1 = loadImage('invader1.png')
invader2 = loadImage('invader2.png')

font_test(mytext)
space_invader_animate([invader1, invader2])
scroll_image_example(mhackspace)

#~ largeScroll(data=mhackspace_multiline, xoffset=pos3, yoffset=1, display=1, left=False)

ser.close()
