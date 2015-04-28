#!/usr/bin/python

"""
Author: Keydrain

Python program for reading values from a USB port and plotting.
Primary use for Collection.ino Arduino program. 

Notes:
Define a queue and use that to plot lines. 
Create multiple queues to create multiple lines. Data needs to be separated 
into elements.
A bit of black magic is included, thanks to matplotlib

"""
 
import sys, serial, argparse, math, select
import datetime
from collections import deque
 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

def timenow():
	"""Used to determine the time for recording and naming data file."""

	now = datetime.datetime.now()
	full = "-%02d-%02d-%02d-%02d" % (int(datetime.date.today().day), 
		int(now.hour), int(now.minute), int(now.second)) 
	return full

FILE = "output" + timenow() + ".csv"

class AnalogPlot:
	"""Generates an Plot according to the matplotlib definition and records
	the data to a file. Also handles sending data to the Arduino.

	Attributes:
		ser: A link to a defined serial port.
		time: A integer for recording when we are.
		ax: The deque that holds the values recorded from the serial.
		maxLen: The number of x values to be present in the graph.
	"""

	def __init__(self, strPort, maxLen):
		"""General initialize code to set most of our values as read in, or 
		zeroed.
		"""

		self.ser = serial.Serial(strPort, 9600)
		self.time = 0.0
		self.ax = deque([0.0]*maxLen)
		self.maxLen = maxLen
 
	def add(self, val):
		"""Added a val to a buf (self.ax) and removes an entry if too many 
		values (this is limited to 600 values or one value per decisecond)
		"""

		if len(self.ax) < self.maxLen:
			self.ax.append(val)
		else:
			self.ax.pop()
			self.ax.appendleft(val)

	def motorOut(self):
		"""If user inputs integer, treat that as number of beads to dispense.
		"""

		while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			line = sys.stdin.readline()
			if line:
				#print("Testing: " + line)
				self.ser.write(str(int(line)))
				#print("Sent:" + line)
			else: # an empty line means stdin has been closed
				break
 
	def update(self, frameNum, al):
		"""The main update function called every 10 ms.
		Calls motorOut.
		Adds the data collected from the serial port and runs runs it through 
		an equation that converts from 0 to 1023 to 0 to 30 for percent of 
		salt. Also, updates the graph and file with the newly added data. 
		"""

		self.time = self.time + 0.1

		self.motorOut()

		try:
			line = self.ser.readline()
			data = int(line)
			data = math.exp((data - 722.86)/16.923)
			#print str(data) + " at " + str(self.time) + " seconds"
			global f
			# Writes to the file
			f.write(str(self.time) + "," + str(data) + "\n")
			self.add(data)
			al.set_data(range(self.maxLen), self.ax)
		except KeyboardInterrupt:
			print('exiting')
		
		return al,

def producePlot():
	"""Produces the final plot from the file including all times with a 
	resolution of deciseconds.
	"""

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
	final = plt.axes(xlim=(0,x[len(x)-1]), ylim=(0,30))
	final.set_title('Arduino Data Collector Results')
	final.set_xlabel('Time in Seconds')
	final.set_ylabel('Salinity Percent (0 to 30')
	final.plot(x, y, 'b')
	plt.show()

def main():
	"""The main function. Sets up the parser, serial, analogPlot, and the 
	main figure. Once the figure is set, begin an animation that attempts to
	pull the serial every 10 milliseconds. This results in a wait as the
	Arduino uploads to serial once every 0.1 seconds.
	"""

	parser = argparse.ArgumentParser(description="LDR serial")
	
	strPort = '/dev/tty.usbmodemfd131'
 
	print('reading from serial port %s...' % strPort)
 
	analogPlot = AnalogPlot(strPort, 600)
 
	print('plotting data... Enter number of beads to dispense: ')
 
	fig = plt.figure()
	ax = plt.axes(xlim=(0, 600), ylim=(0, 30))
	ax.set_title('Arduino Data Collector')
	ax.set_xlabel('Time in Deciseconds')
	ax.set_ylabel('Salinity Percent (0 to 30)')
	al = ax.plot([], [])
	anim = animation.FuncAnimation(fig, analogPlot.update, fargs=al, interval=10)
 
	plt.show()
	
	analogPlot.close()
	f.close()
 
	print('exiting.')
	
if __name__ == '__main__':
	"""Start the program if run under normal conditions. Sets up the file
	globally and places titles on top of the columns on the file. Runs the
	main function and lets that loop until finished. Then produce the final
	plot of all the data. 
	"""

	global f
	f = open(FILE, 'a')
	f.write("Time, Value\n")

	main()

	producePlot()