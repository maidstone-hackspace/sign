import serial
import struct
import time

#dsrdtr setting this true will reset the arduino

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    timeout=0,
    rtscts=True, dsrdtr=True
)

print ser.isOpen()
time.sleep(5)


def stepAll():
    # loop over displays
    for disp in range(0, 2):
        #loop rows
        for a in range(1, 9):
            #loop columns
            for i in range(1, 9):
                offset = (1 << i) - 1
                print offset
                #~ print chr(disp) + chr(a) + chr(offset)
                ser.write(chr(disp) + chr(a) + chr(offset))

                time.sleep(0.05)

square = [
    '00000000',
    '01111110',
    '01000010',
    '01000010',
    '01000010',
    '01000010',
    '01111110',
    '00000000'
]

circle = [
    '00000000',
    '00011000',
    '00100100',
    '01000010',
    '01000010',
    '00100100',
    '00011000',
    '00000000'
]

def drawList(data, display=0):
    for row in range(0, 8):
        offset = int(data[row], 2)
        ser.write(chr(display) + chr(row + 1) + chr(offset))
        s = ser.read(1)
        print(s)

stepAll()
#~ drawList(square, 0)

while True:
    for disp in range(0, 2):
        if disp == 0 :
            
            drawList(square, 0)
            drawList(circle, 1)
        else:
            drawList(circle, 0)
            drawList(square, 1)
        time.sleep(1)

s = ser.read(ser.inWaiting())
#~ ser.write(chr(1) + chr(16))
print(s)
#~ s = ser.read(1)
#~ print(s)
#~ s = ser.read(1)
#~ print(s)
ser.close()
