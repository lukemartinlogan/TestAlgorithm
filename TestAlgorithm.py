"""
This file will use the different location algorithms on
the test data.

RSSI = -65.167 + 10*(-1.889)*log(Distance)
"""

import ast, json, sys
import lmfit, math, numpy as np
import testdata as td

from collections import Counter


prox1 = [(-70, 15), (-60, 7), (-50, 3), (0, 2)]
prox2 = [(-70, 9), (-60, 5), (-50, 2), (0, 1)]

prox3 = [(-76.66666666666667, 15.0), (-70.0, 5.0), (-70.0, 3.0), (0, 1)]
prox4 = [(-90.0, 8.333333333333334), (-70.0, 5.0), (-70.0, 3.0), (0, 1)]
prox5 = [(-76.66666666666667, 15.0), (-70.0, 5.0), (-70.0, 3.0), (0, 1)]
prox6 = [(-76.66666666666667, 15.0), (-70.0, 5.0), (-70.0, 3.0), (0, 1)]

def main():

	#Run the original algorithms over the old test data
	cases = td.TestCases()
	cases.loadCsv1Folder("old_data")
	TestAlgorithm("testresults1_OO.csv", model1, find_floor_simple, prox1, cases)
	TestAlgorithm("testresults2_OO.csv", model2, find_floor_simple, prox2, cases)
	TestAlgorithm("testresults3_OO.csv", model3, find_floor_simple, prox1, cases)
	TestAlgorithm("testresults4_OO.csv", model4, find_floor_simple, prox1, cases)
	
	#Run the new algorithms over the old test data
	TestAlgorithm("testresults1_NO.csv", model1, find_floor_simple, prox3, cases)
	TestAlgorithm("testresults2_NO.csv", model2, find_floor_simple, prox4, cases)
	TestAlgorithm("testresults3_NO.csv", model3, find_floor_simple, prox5, cases)
	TestAlgorithm("testresults4_NO.csv", model4, find_floor_simple, prox6, cases)
	
	#Run original algorithms over the new test data
	cases = td.TestCases()
	cases.downloadTestTable1()
	TestAlgorithm("testresults1_ON.csv", model1, find_floor_simple, prox1, cases)
	TestAlgorithm("testresults2_ON.csv", model2, find_floor_simple, prox2, cases)
	TestAlgorithm("testresults3_ON.csv", model3, find_floor_simple, prox1, cases)
	TestAlgorithm("testresults4_ON.csv", model4, find_floor_simple, prox1, cases)
	
	#Run the new algorithms over the new test data
	TestAlgorithm("testresults1_NN.csv", model1, find_floor_simple, prox3, cases)
	TestAlgorithm("testresults2_NN.csv", model2, find_floor_simple, prox4, cases)
	TestAlgorithm("testresults3_NN.csv", model3, find_floor_simple, prox5, cases)
	TestAlgorithm("testresults4_NN.csv", model4, find_floor_simple, prox6, cases)
	
	

def TestAlgorithm(output, model, floor_model, bins, cases):

	#Set the test case analysis output
	cases.setCsvUrl(output)
	
	for n in range(1,5):
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
		
		#Store a record of the tests
		cases.toCsv()

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