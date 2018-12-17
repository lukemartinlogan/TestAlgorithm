"""
In this file, we test the ability of algorithm
1 to approximate the location of a user based
on bluetooth signals. This is how we do it:
1. Acquire all test cases from the database
2. Run location algorithm on each test case
3. Store a csv of the results of the algorithm
   and the test case information
   
"""

import ast, json, sys
import lmfit, math, numpy as np
import testdata as td

from collections import Counter


proximity_vals = [(-70, 9), (-60, 5), (-50, 2), (0, 1)]

def main():

	#Download all of the test cases
	cases = td.TestCases()
	cases.downloadRecords()
	
	#Set the test case analysis output
	cases.setCsvUrl("testresults2_3_beacons.csv")

	for case in cases:
		#Acquire the positions and signal strengths of the beacons
		(buildings, floors, xs, ys, rssis) = case.getNearestBeaconsAvgMwToDbm(3)
		if(len(buildings) == 0):
			print("No beacons were detected. Continuing")
			continue
		
		#We have 2 parameters (x0, y0), and thus need at least 2 data points
		if(len(buildings) < 2):
			buildings.append(buildings[0])
			floors.append(floors[0])
			xs.append(xs[0])
			ys.append(ys[0])
			rssis.append(rssis[0])
		
		#Convert rssi to proximity
		proximities = getProximity(rssis)
		
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
		flr, bldg = find_floor_simple(floors, buildings)
		
		#Calculate errors
		case.setTestResults(x0, y0, flr)
		
	#Store a record of the tests
	cases.toCsv("testResults_Old.csv")

def getProximity(rssis):
	prox = []
	for rssi in rssis:
		for (sig, dst) in proximity_vals:
			if(rssi < sig):
				prox.append(dst)
				break
	return np.array(prox)

def model(params, x, y, prox):

    x0 = params['x0']
    y0 = params['y0']
    t = np.sqrt((x - x0)**2 + (y - y0)**2)
    t = (prox - t)/prox
	
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