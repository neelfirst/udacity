#!/usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f = open('ep0.25-1000','r')
#f = open('decay-1000','r')
successes = 0.0
failures = 0.0
min_moves = 0.0
num_moves = 0.0
cum_num_moves = 0.0
penalties = 0.0
i = 0
cum_perfects = 0.0

data = pd.DataFrame(np.zeros((1000,7)),columns={'trial','eCSR','eCPR','eOMR','dCSR','dCPR','dOMR'})

for line in f:
	if 'Minimum' in line:
		# first output data
		try:
			data.loc[i,'trial'] = successes+failures
			data.loc[i,'eCSR'] = (successes/(successes+failures))
			data.loc[i,'eCPR'] = (penalties/cum_num_moves)
			if min_moves == num_moves:
				cum_perfects += 1
			data.loc[i,'eOMR'] = cum_perfects
			i += 1
		except:
			print 'exception'
			pass
		# reset variables
#		min_moves = 0.0
#		num_moves = 0.0
#		penalties = 0.0

		# then process new data
		x = line.replace(' ','').split('=')
		try:
			current_min_moves = float(x[-1])
			min_moves = current_min_moves
		except:
			pass

	elif 'Penalties' in line:
		x = line.replace(' ','').split('=')
		penalties += float(x[-1])

	elif 'num moves' in line:
		x = line.replace(' ','').split('=')
		num_moves = float(x[-1])
		cum_num_moves += num_moves

	elif 'Environment' in line:
		if 'aborted' in line:
			failures += 1.0
			num_moves = 5*current_min_moves
			cum_num_moves += num_moves
		elif 'reached' in line:
			successes += 1.0

f = open('decay-1000','r')
successes = 0.0
failures = 0.0
min_moves = 0.0
num_moves = 0.0
cum_num_moves = 0.0
penalties = 0.0
i = 0
cum_perfects = 0.0

for line in f:
	if 'Minimum' in line:
		# first output data
		try:
			data.loc[i,'trial'] = successes+failures
			data.loc[i,'dCSR'] = (successes/(successes+failures))
			data.loc[i,'dCPR'] = (penalties/cum_num_moves)
			if min_moves == num_moves:
				cum_perfects += 1
			data.loc[i,'dOMR'] = cum_perfects
			i += 1
		except:
			print 'exception'
			pass
		# reset variables
#		min_moves = 0.0
#		num_moves = 0.0
#		penalties = 0.0

		# then process new data
		x = line.replace(' ','').split('=')
		try:
			current_min_moves = float(x[-1])
			min_moves = current_min_moves
		except:
			pass

	elif 'Penalties' in line:
		x = line.replace(' ','').split('=')
		penalties += float(x[-1])

	elif 'num moves' in line:
		x = line.replace(' ','').split('=')
		num_moves = float(x[-1])
		cum_num_moves += num_moves

	elif 'Environment' in line:
		if 'aborted' in line:
			failures += 1.0
			num_moves = 5*current_min_moves
			cum_num_moves += num_moves
		elif 'reached' in line:
			successes += 1.0


print data
a = plt.figure()
plt.plot(data['trial'],data['eCSR'],"-",color='red')
plt.plot(data['trial'],data['dCSR'],"-",color='blue')
plt.show()

b = plt.figure()
plt.plot(data['trial'],data['eCPR'],'-',color='red')
plt.plot(data['trial'],data['dCPR'],'-',color='blue')
plt.show()

c = plt.figure()
plt.plot(data['trial'],data['eOMR'],'-',color='red')
plt.plot(data['trial'],data['dOMR'],'-',color='blue')
plt.show()
