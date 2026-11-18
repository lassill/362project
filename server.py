
import socket
import serial #uncomment when pyserial added for microcontroller.

#configuration
HOST = '' #bind to all available interfaces
PORT = 12000

def setup_uart():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    return ser