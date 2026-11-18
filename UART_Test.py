# this file is to test the UART Communication between the server 
# and the STM32

#keyboard interrupt exits program
# MUST have pyserial installed on machine

## UART Setup: UART must be in asynchronous mode, 8 bit word length
# Parity bit set to None, Stop bit set to 1 and Baud Rate 115200


import serial
import time

#edit to match Port and Baud rate configured on STM32
PORT = 'COM3' # change to '/dev/ttyACM0' on mac
BAUD_RATE = 115200

num_blinks = 5; #number of times LED will blink, passed as uint8_t

try:
    #initialize serial connection
    ser = serial.Serial(port = PORT, baudrate= BAUD_RATE, timeout = 1)
    time.sleep(2) # wait time for connection to stabilize

    while True: 
        # 1. Send data to STM32 
        ser.write(num_blinks.to_bytes(2,'little')) 
        # ^ passes number as two bytes with most sig byte at end of array
        # in STM32 HAL_UART_Receive() stores this directly as integer
        print (f"Requested {num_blinks} blinks")

        # 2. check for data in receive buffer
        if ser.in_waiting > 0:
            #read until '\n', decode to string and strip whitespace
            incoming = ser.readline().decode('utf-8', errors = 'ignore'). strip()
            print(f"Received from STM: {incoming}")

        time.sleep(1)
except serial.SerialException as e:
    print(f"Serial Error : {e}")
except KeyboardInterrupt: 
    print("Exiting program ...")
finally:
    #check if serial is created and open before attempting to close it
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed")