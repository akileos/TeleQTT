#!/usr/bin/env python
import serial

class Teleinfo:

        ser = serial.Serial()
        
        def __init__ (self, port='/dev/teleinfo'):
                self.ser = serial.Serial(port, baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN)
        
        def checksum (self, etiquette, valeur):
                sum = 32
                for c in etiquette: sum = sum + ord(c)
                for c in valeur:        sum = sum + ord(c)
                sum = (sum & 63) + 32
                return chr(sum)
                
        def read (self):
                # Wait for data
            while self.ser.inWaiting() : 
                message = ""
                completed = False
                
                while not completed:
                        char = self.ser.read(1)
                        if char != chr(2):
                                message = message + char
                        else:
                                completed = True
                
                frames = [
                        frame.split(" ")
                        for frame in message.strip("\r\n\x03").split("\r\n")
                        ]
                        
                framesOK = dict([
                        [frame[0],frame[1]]
                        for frame in frames
                        if (len(frame) == 3) and (self.checksum(frame[0],frame[1]) == frame[2])
                        ])
                        
                return framesOK
