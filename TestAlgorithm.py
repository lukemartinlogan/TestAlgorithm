"""
This file will use the different location algorithms on
the test data.

RSSI = -65.167 + 10*(-1.889)*log(Distance)
"""

import sys
import lmfit, math, numpy as np
import random
import pandas as pd
from Algorithms import *
from TestData import *


"""
------------------------------------------
This object will be used to represent
individual beacons in a test case.
------------------------------------------
"""

class IBeacon:
	
	def __init__(self, df):
	
		"""
		This function will initialize the beacon information for
		a certain test case.
		
		Inputs:
			df: A pandas dataframe of all of the records of this beacon
			    during the test case
		"""
		
		unique = df[["b_major", "b_minor", "b_x", "b_y", "t_building", "b_floor"]].drop_duplicates().iloc[0]
		self.major = str(unique["b_major"])
		self.minor = str(unique["b_minor"])
		self.key = self.major + self.minor
		self.building = str(unique["t_building"])
		self.floor = int(unique["b_floor"])
		self.x = float(unique["b_x"])
		self.y = float(unique["b_y"])
		self.rssis = []
		self.dbm_sum = 0
		self.mw_sum = 0
		self.dbm_avg = 0
		self.mw_avg = 0
		self.mw_to_dbm_avg = 0
		
		for index, row in df.iterrows():
			self.add_rssi(row["rssi"])
		
	
	def add_rssi(self, rssi):
	
		"""
		This function will add an rssi to the beacon.
		It will also compute the different averages.
		"""
	
		self.rssis.append(rssi)
		self.dbm_sum += rssi
		self.mw_sum += 10**(rssi/10)
		self.dbm_avg = self.dbm_sum/len(self.rssis)
		self.mw_avg = self.mw_sum/len(self.rssis)
		self.mw_to_dbm_avg = 10*np.log10(self.mw_avg)
	
	
	def __str__(self):
		string = "\t\tID: " + str(self.major) + ", " + str(self.minor) + "\n";
		string += "\t\t\t"
		for x in self.rssis:
			string += str(x) + " "
		string += "\n"
		string += "\t\t\tAVG: " + str(self.mw_to_dbm_avg)
		string += "\n"
		return string


"""
------------------------------------------
This object will be used to represent 
individual test cases.
------------------------------------------
"""

class TestCase:

	def __init__(self, df):
		
		"""
		This function will initialize the data for
		a test case.
		
		Inputs:
			df: a dataframe of records who all have the same testid
		"""
		
		unique = df[["testid", "t_building", "t_floor", "t_x", "t_y", "interval"]].drop_duplicates().iloc[0]
		#if(len(unique.index) > 1):
		#	return
		
		self.loc_algorithm = 1
		self.floor_algorithm = 1
		self.bin_strategy = 1
		
		self.testid = str(unique["testid"])
		self.timestamp = str(df["timestamp"].iloc[0])
		self.interval = int(unique["interval"]);
		self.beacons = []
		self.iteration = 0
		self.top_n = 3
		
		self.building_true = int(unique["t_building"]);
		self.floor_true = int(unique["t_floor"]);
		self.x_true = float(unique["t_x"]);
		self.y_true = float(unique["t_y"]);
		
		self.building_est = 0
		self.floor_est = 0
		self.x_est = 0.0
		self.y_est = 0.0
		
		self.xy_error = 0.0
		self.floor_error = 0
		self.building_error = 0
		
		beacons = df[["b_major", "b_minor"]].drop_duplicates()
		for index, b in beacons.iterrows():
			self.beacons.append(IBeacon(df[ (df["b_major"] == b["b_major"]) & (df["b_minor"] == b["b_minor"]) ]))
	
	
	def set_location_algorithm(self, id):
	
		"""
		This function sets the algorithm being used
		in this test case to estimate position.
		
		Inputs:
			id: The algorithm identifier
		"""
	
		self.loc_algorithm = id
	
	
	def set_floor_algorithm(self, id):
		"""
		This function sets the algorithm being used
		to estimate the floor the user is on
		
		Inputs:
			id: The floor algorithm identifier
		"""
		
		self.floor_algorithm = id
	
	
	def set_bin_strategy(self, id):
	
		"""
		This function sets the binning strategy for
		estimating the distance we are from a beacon.
		
		Inputs:
			id: The bin identifier
		"""
	
		self.bin_strategy = id
	
	
	def set_top_n(self, n):
	
		"""
		In the location algorithm, we will estimate
		position using the location of the n
		highest-strength beacons to the tester.
		
		Inputs:
			n: the maximum number of beacons to consider 
			   when estimating position.
		"""
	
		self.top_n = n
	
	
	def estimate_location(self):
		
		#Get the location algorithm
		loc_algorithm = loc_algorithms[self.loc_algorithm]
		
		#Get the floor algorithm
		floor_algorithm = floor_algorithms[self.floor_algorithm]
		
		#Get the binning strategy
		bins = bin_strategies[self.bin_strategy]

		#Acquire the positions and signal strengths of the beacons
		(buildings, floors, xs, ys, rssis) = self.getNearestBeaconsAvgMwToDbm()
		if(len(buildings) == 0):
			print("No beacons were detected in this test case.")
			return
		
		#We have 2 parameters (x0, y0), and thus need at least 2 data points (beacons)
		if(len(buildings) < 2):
			buildings.append(buildings[0])
			floors.append(floors[0])
			xs.append(xs[0])
			ys.append(ys[0])
			rssis.append(rssis[0])
		
		#Convert rssi to proximity
		proximities = self.getProximity(bins, rssis)
		
		# defining our final x0 and y0 parameters that we minimize.
		params = lmfit.Parameters()
		params.add('x0', value=0)
		params.add('y0', value=0)
		
		#Estimate position on floor
		mini = lmfit.Minimizer(loc_algorithm, params, fcn_args=(xs, ys, proximities))
		result = mini.minimize()
		x0 = result.params['x0'].value
		y0 = result.params['y0'].value
		
		#Estimate floor
		flr, bldg = floor_algorithm(floors, buildings)
		
		#Calculate errors
		self.setTestResults(x0, y0, flr, bldg)
	
	
	def avgMwToDbm(self, beacon):
	
		"""
		This is a callback function.
		It's used to sort beacons by mw_to_dbm_avg.
		
		Input:
			beacon: The IBeacon that we are getting mw_to_dbm_avg from
		Return:
			This function will return the average of RSSI after converting
			to dBm.
		"""
	
		return beacon.mw_to_dbm_avg
	
		
	def getNearestBeaconsAvgMwToDbm(self):
	
		"""
		This function will acquire the beacons whose
		average rssi was computed by averaging power
		and then converting from power to dbm.
		"""
		
		self.beacons.sort(reverse = True, key = self.avgMwToDbm)
		subset = self.beacons[0:self.top_n]
		
		buildings = []
		floors = []
		xs = []
		ys = []
		rssis = []
		
		for beacon in subset:
			buildings.append(beacon.building)
			floors.append(beacon.floor)
			xs.append(beacon.x)
			ys.append(beacon.y)
			rssis.append(beacon.mw_to_dbm_avg)
		
		return (buildings, floors, xs, ys, rssis)
	
	
	def getProximity(self, bins, rssis):
	
		"""
		This function will map RSSI to
		distance using a binning strategy.
		
		Inputs:
			bins: The bins to use when mapping RSSI to distance
			rssis: The set of rssis to map to distance
		Return:
			A numpy array of distances
		"""
	
		prox = []
		for rssi in rssis:
			for (sig, dst) in bins:
				if(rssi < sig):
					prox.append(dst)
					break
		return np.array(prox)
	
		
	def setTestResults(self, x_est, y_est, floor_est, building_est):
	
		"""
		This function will set the results of a test.
		It will compute the error of the estimate.
		
		Inputs:
			x_est: The estimated x-coordinate of the user
			y_est: The estimated y-coordinate of the user
			floor_est: The estimated floor the user is on
			building_est: The estimated building the user is on
		"""
		
		self.x_est = x_est
		self.y_est = y_est
		self.floor_est = floor_est
		self.building_est = building_est
		
		self.xy_error = ((self.x_true - self.x_est)**2 + (self.y_true - self.y_est)**2)**.5
		self.floor_error = abs(floor_est - self.floor_true)
		self.building_error = building_est != self.building_true
			
	
	def __iter__(self):
	
		"""
		This will initialize an iteration
		of all beacons over this object.
		"""
	
		self.iteration = iter(self.beacons)
		return self
	
	
	def __next__(self):
	
		"""
		This will acquire the next beacon
		in an iteration.
		"""
	
		return self.iteration.next()
		
	
	def __str__(self):
		string = ""
		string += "Test ID: " + str(self.test_id) + "\n"
		string += "\tBuilding: " + str(self.building) + "\n"
		string += "\tFloor: " + str(self.floor_true) + "\n"
		string += "\tPosition: (" + str(self.x_true) + ", " + str(self.y_true) + ")\n"
		string += "\tInterval: " + str(self.interval) + "\n"
		string += "\tTop N Beacons: " + str(self.top_n) + "\n"
		string += "\tBEACONS:\n"
		for beacon in self.beacons:
			string += str(beacon)
		string += "\n"
		string += "Floor Estimate: " + str(self.floor_est) + "\n"
		string += "Position Estimate: (" + str(self.x_est) + ", " + str(self.y_est) + ")\n"
		string += "Error: " + str(self.error) + "\n"
		
		return string

		
	def to_csv_record(self):
	
		"""
		This function will convert a test case to a record of the following form:
				
		[testid][timestamp][interval][loc_alg][floor_alg][bin_strat][top_n]
		[building_true][floor_true][x_true][y_true]
		[building_est][floor_est][x_est][y_est]
		[building_error][floor_error][xy_error]
		"""
		
		s = ""
		s += str(self.testid) + ","
		s += str(self.timestamp) + ","
		s += str(self.interval) + ","
		s += str(self.loc_algorithm) + ","
		s += str(self.floor_algorithm) + ","
		s += str(self.bin_strategy) + ","
		s += str(self.top_n) + ","
		s += str(self.building_true) + ","
		s += str(self.floor_true) + ","
		s += str(self.x_true) + ","
		s += str(self.y_true) + ","
		s += str(self.building_est) + ","
		s += str(self.floor_est) + ","
		s += str(self.x_est) + ","
		s += str(self.y_est) + ","
		s += str(self.building_error) + ","
		s += str(self.floor_error) + ","
		s += str(self.xy_error)
		
		return s
				

"""
------------------------------------------
This object will be a set of test cases
that the algorithms can estimate position
with.
------------------------------------------
"""

class TestCases:
	
	def __init__(self, out = "results.csv", append = False):
		self.out_path = out
		self.append = append
		self.out = None
		self.header = not append
		self.test_data = None
		self.test_ids = None
		self.test_cases = []
		
		self.net_xy_error = 0
		self.net_floor_error = 0
		self.net_building_error = False
	
	
	def open_test_data(self, path = "database.csv", building = None, floor = None, sample=None, interval=None):
	
		"""
		This function will load the test data for algorithm analysis.
		
		Inputs:
			path: the location of the test data
			building: the building we are interested in
			floor: the floor of that building we are interested in
			sample: select a random sample of the test data
			interval: select only test cases for a certain interval
		"""
	
		#Open the CSV of test data
		self.test_data = pd.read_csv(path)
		
		#Select test data from this building
		if building is not None:
			building_code = BuildingStrToCode[building]
			self.test_data = self.test_data[self.test_data["t_building"] == building_code]
			
		#Select test data from this floor of the building
		if floor is not None:
			self.test_data = self.test_data[self.test_data["t_floor"] == floor]
		
		#Select test data taken for this interval
		if interval is not None:
			self.test_data = self.test_data[self.test_data["interval"] == interval]
		
		
		#Get the test case ids
		self.test_ids = self.test_data["testid"].drop_duplicates()
		if sample is not None:
			self.test_ids = self.test_ids.sample(n=sample, axis=0)
		
		#Iterate over each test case id
		i = 0
		for id in self.test_ids:
			self.test_cases.append(TestCase(self.test_data[self.test_data["testid"] == id]))
	
	
	def reset(self):
	
		"""
		Resets the error metrics.
		"""
	
		self.net_xy_error = 0
		self.net_floor_error = 0
		self.net_building_error = False
	
	
	def test_algorithm(self, loc_alg = 2, floor_alg = 1, bin_strategy = 1, top_n = 3):
	
		"""
		This function will estimate the indoor location of a user
		at the test positions defined in the test data.
		"""
	
		for case in self.test_cases:
			case.set_location_algorithm(loc_alg)
			case.set_floor_algorithm(floor_alg)
			case.set_bin_strategy(bin_strategy)
			case.set_top_n(top_n)
			case.estimate_location()
			
			self.net_xy_error += case.xy_error
			self.net_floor_error += case.floor_error
			self.net_building_error += case.building_error

	
	def optimize_bins(self, loc_alg=2, floor_alg=1, top_n=3, num_guesses = 1000):
	
		"""
		This function will optimize the bins for a certain
		set of test data.
		
		It randomly guesses the bin size and recomputes
		the error produced by the algorithm using this
		bin strategy.
		"""
	
		min_err = np.inf
		min_bin = None
		
		for i in range(0, num_guesses):
		
			#r values are changes in rssi between the bins
			r2 = random.randint(-70, -10)
			r3 = random.randint(-70, -10)
			r4 = random.randint(-70, -10)
			
			#d values are changes in distance between the bins
			d1 = random.randint(1, 10)
			d2 = random.randint(1, 10)
			d3 = random.randint(1, 10)
			d4 = random.randint(1, 10)
		
			#This guesses the bin
			bin_strategies[-1] = [
				(r2 + r3 + r4, d1+d2+d3+d4),
				(r2 + r3, d1+d2+d3),
				(r2, d1+d2),
				(0, d1)
			]
			
			#Test the algorithm with this new strategy
			self.reset()
			self.test_algorithm(loc_alg=loc_alg, floor_alg=floor_alg, bin_strategy=len(bin_strategies)-1, top_n=top_n)
			if self.net_xy_error < min_err:
				min_bin = bin_strategies[-1]
				min_err = self.net_xy_error
			
			sys.stdout.write(str((i+1)/num_guesses) + "\r")
		
		print("Minimum error: " + str(min_err))
		print("Bin strategy: ", str(min_bin))
	
	
	def to_csv(self):
	
		"""
		This function will output the result of the indoor location
		algorithm.
		"""
	
		if self.out is None:
			if self.append:
				self.out = open(self.out_path, "a")
			else:
				self.out = open(self.out_path, "w")
		
		s = ""
		if self.header:
			s += "testid,timestamp,interval,loc_alg,floor_alg,bin_strat,top_n,"
			s += "building_true,floor_true,x_true,y_true,"
			s += "building_est,floor_est,x_est,y_est,"
			s += "building_error,floor_error,xy_error" + "\n"
			self.header = False
		
		for case in self.test_cases:
			s += case.to_csv_record() + "\n"
		
		self.out.write(s)



	
