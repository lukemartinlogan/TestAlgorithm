"""
This file will use the different location algorithms on
the test data.

RSSI = -65.167 + 10*(-1.889)*log(Distance)
"""

import sys
import lmfit, math, numpy as np
import random
import pandas as pd
from progressbar import ProgressBar
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
		self.building = int(unique["t_building"])
		self.floor = int(unique["b_floor"])
		self.x = float(unique["b_x"])
		self.y = float(unique["b_y"])
		self.rssis = np.array(df["rssi"])
		self.dbm_sum = self.rssis.sum()
		self.mw_sum = (10**(self.rssis/10)).sum()
		self.dbm_avg = self.dbm_sum/len(self.rssis)
		self.mw_avg = self.mw_sum/len(self.rssis)
		self.mw_to_dbm_avg = 10*np.log10(self.mw_avg)


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
			self.beacons.append(
				IBeacon(df[ 
					(df["b_major"] == b["b_major"]) & 
					(df["b_minor"] == b["b_minor"])
				]))
	
	
	def set_location_algorithm(self, loc_alg):
	
		"""
		This function sets the algorithm being used
		in this test case to estimate position.
		
		Inputs:
			loc_alg: An id in the loc_algorithm dictionary in Algorithms.py
		"""
		
		self.loc_algorithm = (loc_alg, loc_algorithms[loc_alg])
	
	
	def set_floor_algorithm(self, floor_alg):
		"""
		This function sets the algorithm being used
		to estimate the floor the user is on
		
		Inputs:
			floor_alg: An id in the floor_algorithms dictionary in Algorithms.py
		"""
		
		self.floor_algorithm = (floor_alg, floor_algorithms[floor_alg])
	
	
	def set_bin_strategy(self, bin_strategy):
	
		"""
		This function sets the binning strategy for
		estimating the distance we are from a beacon.
		
		Inputs:
			bin_strategy: An id in the bin_strategies dictionary in Algorithms.py
		"""
		
		self.bin_strategy = (bin_strategy, bin_strategies[bin_strategy])
	
	
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
		loc_algorithm = self.loc_algorithm[1]
		
		#Get the floor algorithm
		floor_algorithm = self.floor_algorithm[1]
		
		#Get the binning strategy
		bins = self.bin_strategy[1]

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
		flr, bldg = floor_algorithm(floors, proximities, buildings)
		
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
	
	
	def get_record(self):
	
		"""
		This function will convert a test case to a record of the following form:
				
		[testid][timestamp][interval][loc_alg][floor_alg][bin_strat][top_n]
		[building_true][floor_true][x_true][y_true]
		[building_est][floor_est][x_est][y_est]
		[building_error][floor_error][xy_error]
		"""
		
		record = {
			"testid": self.testid,
			"timestamp": self.timestamp,
			"interval": self.interval,
			"loc_alg": self.loc_algorithm[0],
			"floor_alg": self.floor_algorithm[0],
			"bin_strat": self.bin_strategy[0],
			"top_n": self.top_n,
			"building_true": self.building_true,
			"floor_true": self.floor_true,
			"x_true": self.x_true,
			"y_true": self.y_true,
			"building_est": self.building_est,
			"floor_est": self.floor_est,
			"x_est": self.x_est,
			"y_est": self.y_est,
			"building_error": self.building_error,
			"floor_error": self.floor_error,
			"xy_error": self.xy_error
		}
		
		return record
				

"""
------------------------------------------
This object will be a set of test cases
that the algorithms can estimate position
with.
------------------------------------------
"""

class TestCases:
	
	def __init__(self, out = "Datasets/results.csv", append = False):
	
		"""
		This will initialize the variables used in this
		object.
		
		Inputs:
			out: The location to save test results to
			append: Whether or not the results file should be overwritten
		"""
	
		self.out_path = out
		self.append = append
		self.test_data = None
		self.test_ids = None
		self.test_cases = None
		
		self.net_xy_error = 0
		self.net_floor_error = 0
		self.net_building_error = False
	
	
	def open_test_data(
		self, database = "Datasets/database.csv", results = None, 
		building = None, floor = None, sample=None, 
		interval=None, loc_alg=2, floor_alg=1, bin_strategy=3, top_n=3
		):
	
		"""
		This function will load the test data for algorithm analysis.
		It will also load the results of a previous analysis if given.
		
		Inputs:
			database: the location of the test data
			results: the path to the previous analysis
			building: the building we are interested in (string)
			floor: the floor of that building we are interested in
			sample: select a random sample of the test data (this  is a number)
			interval: select only test cases for a certain interval
			loc_alg: The location algorithm used to get results
			floor_alg: The floor algorithm used to get results
			bin_strategy: The binning strategy used to get results
			top_n: The number of beacons used to get results
		"""
	
		#Open the CSV of test data
		self.test_data = pd.read_csv(database)
		
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
		self.test_ids = self.test_data[["testid", "t_x", "t_y", "t_floor", "t_building"]].drop_duplicates()
		if sample is not None:
			if sample > len(self.test_ids):
				sample = len(self.test_ids)
			self.test_ids = self.test_ids.sample(n=sample, axis=0)
		
		#Get data for each unique test case
		i = 0
		self.test_cases = {}
		for index, id in self.test_ids.iterrows():
			key = str(id["testid"]) + str(id["t_x"]) + str(id["t_y"]) + str(id["t_floor"]) + str(id["t_building"])
			self.test_cases[key] = TestCase(
				self.test_data[
					(self.test_data["testid"] == id["testid"]) &
					(self.test_data["t_x"] == id["t_x"]) &
					(self.test_data["t_y"] == id["t_y"]) &
					(self.test_data["t_floor"] == id["t_floor"]) &
					(self.test_data["t_building"] == id["t_building"])
				]
			)
		
		#Load results for the test cases
		if results:
			self.open_results(results, interval, loc_alg, floor_alg, bin_strategy, top_n)
	
	
	def open_test_cases(
		self, cases, database = "Datasets/database.csv", results=None, 
		interval=10, loc_alg=2, floor_alg=1, bin_strategy=3, top_n=3
	):
		
		"""
		This function will load a subset of test cases for algorithm analysis
		
		Inputs:
			cases: a list of test IDs
			database: the location of the test data
			results: the path to the previous analysis
			interval: The scanning period used to get results
			loc_alg: The location algorithm used to get results
			floor_alg: The floor algorithm used to get results
			bin_strategy: The binning strategy used to get results
			top_n: The number of beacons used to get results
		"""
		
		self.test_data = pd.read_csv(database)
		cases = dict(zip(cases, [None]*len(cases)))
		
		#Get the test case ids
		self.test_ids = self.test_data[["testid", "t_x", "t_y", "t_floor", "t_building"]].drop_duplicates()
		
		#Get data for each unique test case
		i = 0
		self.test_cases = {}
		for index, id in self.test_ids.iterrows():
			if id["testid"] not in cases:
				continue
			key = str(id["testid"]) + str(id["t_x"]) + str(id["t_y"]) + str(id["t_floor"]) + str(id["t_building"])
			self.test_cases[key] = TestCase(
				self.test_data[
					(self.test_data["testid"] == id["testid"]) &
					(self.test_data["t_x"] == id["t_x"]) &
					(self.test_data["t_y"] == id["t_y"]) &
					(self.test_data["t_floor"] == id["t_floor"]) &
					(self.test_data["t_building"] == id["t_building"])
				]
			)
		
		#Load results for the test cases
		if results:
			self.open_results(results, interval, loc_alg, floor_alg, bin_strategy, top_n)
	
	
	def open_results(self, results, interval=10, loc_alg=2, floor_alg=1, bin_strategy=3, top_n=3):
		
		"""
		This function will load the results from a previous analysis.
		You MUST have called open_test_data or open_test_cases before this.
		
		Inputs:
			results: the path to the previous analysis
			interval: The scanning period used to get results
			loc_alg: The location algorithm used to get results
			floor_alg: The floor algorithm used to get results
			bin_strategy: The binning strategy used to get results
			top_n: The number of beacons used to get results
		"""
		
		results = pd.read_csv(results)
		results = results[
			(results["interval"] == interval) &
			(results["loc_alg"] == loc_alg) &
			(results["floor_alg"] == floor_alg) &
			(results["bin_strat"] == bin_strategy) &
			(results["top_n"] == top_n)
		]
		for index, id in results.iterrows():
			#Get case
			key = str(id["testid"]) + str(id["x_true"]) + str(id["y_true"]) + str(id["floor_true"]) + str(id["building_true"])
			if key not in self.test_cases.keys():
				continue
			case = self.test_cases[key]
			
			#Load results
			case.building_est = id["building_est"]
			case.floor_est = id["floor_est"]
			case.x_est = id["x_est"]
			case.y_est = id["y_est"]
			case.building_error = id["building_error"]
			case.floor_error = id["floor_error"]
			case.xy_error = id["xy_error"]
	
	
	def reset(self):
	
		"""
		Resets the test results.
		"""
	
		self.net_xy_error = 0
		self.net_floor_error = 0
		self.net_building_error = False
	
	
	def test_algorithm(self, loc_alg, floor_alg, bin_strategy, top_n = 3, to_csv=True):
	
		"""
		This function will estimate the indoor location of a user
		at the test positions defined in the test data.
		
		Inputs:
			loc_alg: An index into the loc_algorithms array in Algorithms.py 
			floor_alg: An index into the floor_algorithms array in Algorithms.py 
			bin_strategy: An index into the bin_strategies array in Algorithms.py
			top_n: The number of beacons to consider when making location estimates
			to_csv: Whether or not to save the results to the CSV file
		"""
		
		self.reset()
		for case in self.test_cases.values():
			case.set_location_algorithm(loc_alg)
			case.set_floor_algorithm(floor_alg)
			case.set_bin_strategy(bin_strategy)
			case.set_top_n(top_n)
			case.estimate_location()
			self.net_xy_error += case.xy_error
			self.net_floor_error += case.floor_error
			self.net_building_error += case.building_error
		
		if to_csv:
			self.to_csv()	
	
	
	def to_csv(self):
	
		"""
		This function will output the result of the indoor location
		algorithm.
		"""
	
		col = [
			"testid", "timestamp", "interval", "loc_alg", "floor_alg", "bin_strat", "top_n",
			"building_true", "floor_true", "x_true", "y_true",
			"building_est", "floor_est", "x_est", "y_est",
			"building_error", "floor_error", "xy_error"
		]
		
		#Pack test results
		self.df = pd.DataFrame(columns=col)
		for case in self.test_cases.values():
			self.df = self.df.append(case.get_record(), ignore_index=True)
		
		#Commit results
		if self.append and os.path.exists(self.out_path):
			self.df.to_csv(self.out_path, mode='a', header=False, index=False)	
		else:
			self.df.to_csv(self.out_path, mode='w', header=True, index=False)
		

	
	




