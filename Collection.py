#!/usr/bin/python

"""
Author: Keydrain

Python program for reading values from a USB port and plotting.
Primary use for Collection.ino Arduino program. 

Notes:
Define a queue and use that to plot lines. 
Create multiple queues to create multiple lines. Data needs to be separated into elements.
A bit of black magic is included, thanks to matplotlib

Note on Dispenser:
Use Pot to specify speed, with LED's to represent rate.
Use safety switch to pass values to the motor.
Possibly binary representation of the rate to use LED's efficiently. 

"""
 
import sys, serial, argparse
import numpy as np
from time import sleep
import datetime
from collections import deque
 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

def timenow():
	now = datetime.datetime.now()
	full = "-%02d-%02d-%02d-%02d" % (int(datetime.date.today().day), 
		int(now.hour), int(now.minute), int(now.second)) 
	return full

FILE = "output" + timenow() + ".csv"

class AnalogPlot:
	def __init__(self, strPort, maxLen):
		self.ser = serial.Serial(strPort, 9600)
		self.time = 0.0
		self.ax = deque([0.0]*maxLen)
		self.maxLen = maxLen
 
	def addToBuf(self, buf, val):
		if len(buf) < self.maxLen:
			buf.append(val)
		else:
			buf.pop()
			buf.appendleft(val)
 
	def add(self, data):
			self.addToBuf(self.ax, data)
 
	def update(self, frameNum, al):
		self.time = self.time + 0.1

		try:
			line = self.ser.readline()
			data = int(line)
			print str(data) + " at " + str(self.time) + " seconds"
			global f
			f.write(str(self.time) + "," + str(data) + "\n")
			self.add(data)
			al.set_data(range(self.maxLen), self.ax)
		except KeyboardInterrupt:
			print('exiting')
		
		return al,
 
	def close(self):
		self.ser.flush()
		self.ser.close()

def producePlot():
	x = []
	y = []
	lines = open(FILE, 'r').read().splitlines()
	for row in lines:
		work = row.split(',')
		try:
			x.append(float(work[0]))
			y.append(float(work[1]))
		except:
			None
	fig = plt.figure()
	final = plt.axes(xlim=(0,x[len(x)-1]), ylim=(0,1023))
	final.set_title('Arduino Data Collector Results')
	final.set_xlabel('Time in Seconds')
	final.set_ylabel('Voltage Divider (0 to 1023')
	final.plot(x, y, 'b')
	plt.show()


def main():
	parser = argparse.ArgumentParser(description="LDR serial")
	
	strPort = '/dev/tty.usbmodemfd131'
 
	print('reading from serial port %s...' % strPort)
 
	analogPlot = AnalogPlot(strPort, 600)
 
	print('plotting data...')
 
	fig = plt.figure()
	ax = plt.axes(xlim=(0, 600), ylim=(0, 1023))
	ax.set_title('Arduino Data Collector')
	ax.set_xlabel('Time in Deciseconds')
	ax.set_ylabel('Voltage Divider (0 to 1023)')
	al = ax.plot([], [])
	anim = animation.FuncAnimation(fig, analogPlot.update, fargs=al, interval=10)
 
	plt.show()
	
	analogPlot.close()
	f.close()
 
	print('exiting.')
	
if __name__ == '__main__':
	global f
	f = open(FILE, 'a')
	f.write("Time, Value\n")

	main()

	producePlot()