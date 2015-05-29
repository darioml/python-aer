import math
import numpy as np

import os, datetime

from pprint import pprint

class pAER:
	def __init__(self, filename, max_events=1e6):

		with open(filename, 'r') as f:
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
			
			if numEvents > max_events:
				print 'There are %i events, but max_events is set to %i. Will only use %i events.' % (numEvents, max_events, max_events)
				numEvents = max_events

			f.seek(current)

			aerTimestamp = np.zeros( numEvents )
			aerData      = np.zeros( numEvents )

			for i in range(numEvents):
				
				aerTimestamp[i] = int(f.read(4).encode('hex'), 16)
				aerData[i]      = int(f.read(4).encode('hex'), 16)

			pprint(aerData)
			pprint(aerTimestamp)



		
		print
		print max_events


if __name__ == "__main__":
	hello = pAER('/Users/darioml/src/fyp-aedata-matlab/test.aedat', max_events=2)
	print "test"
