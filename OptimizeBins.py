
"""
This file will optimize the bins for a certain
algorithm over a data set

RSSI = -65.167 + 10*(-1.889)*log(Distance)

"""

import ast, json, sys
import lmfit, math, numpy as np
import testdata as td
from scipy.optimize import minimize

from collections import Counter


prox1 = [(-70, 15), (-60, 7), (-50, 3), (0, 2)]
prox2 = [(-70, 9), (-60, 5), (-50, 2), (0, 1)]

def main():
	
	#Run the algorithms over test data
	cases = td.TestCases()
	cases.downloadTestTable1()
	#cases.loadCsv1Folder("old_data")
	
	#Optimize bins to new data set
	OptimizeBinsForAlgorithm(model1, find_floor_simple, cases)
	OptimizeBinsForAlgorithm(model2, find_floor_simple, cases)
	OptimizeBinsForAlgorithm(model3, find_floor_simple, cases)
	OptimizeBinsForAlgorithm(model4, find_floor_simple, cases)

def OptimizeBinsForAlgorithm(model, floor_model, cases):
	
	min_err = np.inf
	min_bin = None
	step = 5
	step2 = 5
	
	#Change the signal strength size for the bins
	for i in range(1, step):
		for j in range(1, step):
			for k in range(1, step):
				for L in range(1, step2):
					for m in range(1, step2):
						for n in range(1, step2):
							bins = [
								(-70 - 20/i, 5 + 10/L),
								(-60 - 20/j, 3 + 8/m),
								(-50 - 20/k, 0 + 3/n),
								(0, 1)
							]
							if(bins[0][0] > bins[1][0]):
								continue
							if(bins[1][0] > bins[2][0]):
								continue
							if(bins[0][1] < bins[1][1]):
								continue
							if(bins[1][1] < bins[2][1]):
								continue
							if(bins[2][1] < bins[3][1]):
								continue
							
							err = FitAlgorithm(model, floor_model, bins, cases)
							if err < min_err:
								min_bin = bins
								min_err = err
							
							num = step*step*step2**3*i + step*step2**3*j + k*step2**3 + L*step2**2 + m*step2 + n
							#print(str(num/(step**3 * step2**3)))
	
	print(min_err)
	print(min_bin)

def FitAlgorithm(model, floor_model, bins, cases):
	
	error = 0
	for n in range(3,4):
		for case in cases:
			#Acquire the positions and signal strengths of the beacons
			(buildings, floors, xs, ys, rssis) = case.getNearestBeaconsAvgMwToDbm(n)
			if(len(buildings) == 0):
				print("No beacons were detected. Continuing")
				continue
			
			#We have 2 parameters (x0, y0), and thus need at least 2 data points (beacons)
			if(len(buildings) < 2):
				buildings.append(buildings[0])
				floors.append(floors[0])
				xs.append(xs[0])
				ys.append(ys[0])
				rssis.append(rssis[0])
			
			#Convert rssi to proximity
			proximities = getProximity(bins, rssis)
			
			# defining our final x0 and y0 parameters that we minimize.
			params = lmfit.Parameters()
			params.add('x0', value=0)
			params.add('y0', value=0)
			
			#Estimate position on floor
			mini = lmfit.Minimizer(model, params, fcn_args=(xs, ys, proximities))
			result = mini.minimize()
			x0 = result.params['x0'].value
			y0 = result.params['y0'].value
			
			#Estimate floor
			flr, bldg = floor_model(floors, buildings)
			
			#Calculate errors
			case.setTestResults(x0, y0, flr)
			error += case.error
	
	return error

def getProximity(bins, rssis):
	prox = []
	for rssi in rssis:
		for (sig, dst) in bins:
			if(rssi < sig):
				prox.append(dst)
				break
	return np.array(prox)

def model1(params, x, y, prox):
    x0 = params['x0']
    y0 = params['y0']
    t = (x - x0)**2 + (y - y0)**2
    t = (t - prox)/prox
	
    return t

def model2(params, x, y, prox):

    x0 = params['x0']
    y0 = params['y0']
    t = np.sqrt((x - x0)**2 + (y - y0)**2)
    t = (prox - t)/prox
	
    return t

def model3(params, x, y, prox):
    x0 = params['x0']
    y0 = params['y0']
    t = np.sqrt((x - x0)**2 + (y - y0)**2)
    t = t/prox**2
	
    return t

def model4(params, x, y, prox):
    x0 = params['x0']
    y0 = params['y0']
    t = (x - x0)**2 + (y - y0)**2
    t = t/prox**2
	
    return t
	
def find_floor_simple(floor, building_id):
    # making a list of tuples (floor, building_id)
    zipped = list(zip(floor, building_id))
    
    # counter object that has key(tuple) and value(count)
    c = Counter(x for x in zipped)
    
    # getting the 1 most common keys, gets a list of tuples(key, count) return the first tuple's key   
    return c.most_common(1)[0][0]

if __name__ == "__main__":
	main()

