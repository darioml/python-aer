import math
import numpy as np

import os, datetime

from pprint import pprint

import matplotlib.pyplot as plt


class pAER:
	def __init__(self, filename, max_events=1e6):
		self.filename = filename
		self.max_events = max_events
		self.load()

	def load(self):
		with open(self.filename, 'r') as f:
			line = f.readline()
			while (line[0] == '#'):
				if (line[0:9] == '#!AER-DAT'):
					aer_version = line[9];
				current = f.tell();
				line = f.readline()


			if (aer_version != '2'):
				raise Exception('Invalid AER version. Expected 2, got %s' % aer_version)

			f.seek(0,2)
			numEvents = math.floor( ( f.tell() - current ) / 8 )
			
			if numEvents > self.max_events:
				print 'There are %i events, but max_events is set to %i. Will only use %i events.' % (numEvents, self.max_events, self.max_events)
				numEvents = self.max_events

			f.seek(current)

			self.timestamps = np.zeros( numEvents )
			self.data       = np.zeros( numEvents )

			for i in range(numEvents):

				self.data[i] = int(f.read(4).encode('hex'), 16)
				self.timestamps[i]       = int(f.read(4).encode('hex'), 16)

			return self

	def unpackData(self, data):
		noData = len(data)
		
		x = np.zeros(noData)
		y = np.zeros(noData)
		t = np.zeros(noData)

		for i in range(1):
			d = int(data[i])
			
			t[i] = d & 0x1			
			x[i] = (d >> 0x1) & 0x7F
			y[i] = (d >> 0x8) & 0x7F
		return (x,y,t)


if __name__ == "__main__":
	hello = pAER('/Users/darioml/src/fyp-aedata-matlab/test.aedat', max_events=10)

	(x,y,t) = hello.unpackData(hello.data)


	plt.plot(y,x)
	plt.show()
