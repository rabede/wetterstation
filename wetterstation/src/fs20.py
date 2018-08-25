#!/usr/bin/python3
from serial import Serial


ser = Serial('/dev/ttyAMA0',4800)

ser.write("0202fb01")
ser.write("0202f201")

try:
	while 1:
		line=ser.readline()
		name,value=line.split(": ")
		if name == "Temperatur":
			temp,hex=value.split(" C")
			print(temp)
		elif name == "Luftfeuchtigkeit":
			hum,hex=value.split(" %")
			print(hum)
		elif name == "Windgeschw.":
			vel,hex=value.split(" km/h")
			print(vel)
		elif name == "Niederschlag":
			down,hex=value.split(" (")
			print(down)
		elif name == "Regen":
			rain,hex=value.split(" (")
			print(rain)
		f=open('tempLog.dat','a')
		print(line)
		print >>f,(line)
		f.close()
except KeyboardInterrupt:
	print("\ndone")