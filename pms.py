import serial

# we stop terminal with raspi-config,
# we stop bluethooth from /boot/config.txt first,
# and currently UART device is /dev/ttyAMAO,
# but we still cannot read data from device

# failure devices
#dev = "ttyS0"

# work devices
#dev = "ttyAMA0"
#dev = "serial0"
dev = "ttyUSB0"

ser = serial.Serial(port="/dev/"+dev,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS, timeout=2)
while True:
    data = ser.read()
    print str(data), len(data)
ser.close()
