#!/usr/bin/python

import serial, time, sys
from aidon.aidon_obis import *

def aidon_callback(fields):
	print (fields)

def main():

	if len (sys.argv) != 2:
		print( "Usage: ... <serial_port>")
		sys.exit(0)

	ser = serial.Serial(sys.argv[1], 115200, timeout=0.05, parity=serial.PARITY_NONE)
	a = aidon(aidon_callback)

	while(1):
		while ser.inWaiting():
			a.decode(ser.read(1))
		time.sleep(0.01)

if __name__ == "__main__":
	main()
