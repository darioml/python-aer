import math
import numpy as np

import os, datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib  import cm


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

		for i in range(noData):
			d = int(data[i])
			
			t[i] = d & 0x1			
			x[i] = 128-((d >> 0x1) & 0x7F)
			y[i] = (d >> 0x8) & 0x7F
		return (x,y,t)

	def interactiveAnimation(self,data,step=5000):
		plt.ion()
		fig = plt.figure(figsize=(6,6))
		plt.show()

		ax = fig.add_subplot(111)
		ax.set_xlim(0,128)
		ax.set_ylim(0,128)

		start = 0;
		end = step-1;
		ax.scatter(x[start:end],y[start:end],s=20,c=t[start:end], marker = 'o', cmap = cm.jet );

		for i in range(200):
			ax.clear()
			ax.set_xlim(0,128)
			ax.set_ylim(0,128)
			ax.scatter(x[start:end],y[start:end],s=20,c=t[start:end], marker = 'o', cmap = cm.jet );
			start = start + step;
			end   = end   + step;
			plt.draw()

	# def betterAnimation(self,data,step=5000):
		# start = 0;
		# step = 5000;
		# end = step-1;

		# fig, ax = plt.subplots()
		# ax.set_xlim(0,128)
		# ax.set_ylim(0,128)

		# scatt = ax.scatter(x[start:end],y[start:end],s=20,c=t[start:end], marker = 'o', cmap = cm.jet );

		# def update(data):

		# 	# scatt.set_color(c=data)
		# 	scatt.set_offsets(data)

		# 	# start = start + 5000;
		# 	# end   = end   + 5000;
		# 	# line.set_ydata(data)
		# 	return scatt

		# def data_gen():
		# 	start = 0;
		# 	step = 5000;
		# 	end = step-1;
		# 	while True: 
		# 		data = (x[start:end],y[start:end])
		# 		start = start + 5000;
		# 		end   = end   + 5000;
		# 		yield data
		# 		 # 128*np.random.rand(5000,1)

		# ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
		# plt.show()


