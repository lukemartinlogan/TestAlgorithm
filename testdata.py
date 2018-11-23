
"""
This file acquires test cases from the database and
puts them into a meaningful format. 

NOTE: this file assumes that the beacon positions 
are NOT stored in the test table.

table schemas:
	test data table: [testid][beacon_major][beacon_minor][building_id][floor][x][y][rssi][interval][id][timestamp]
	beacon table:	 [beacon_id][major][minor][building_id][floor][x][y][loc_id][temperature][humidity][updatetimestamp]
	
csv schema: [testid][beacon_major][beacon_minor][b_building][b_floor][b_x][b_y][rssi][duration][building][floor_true][x_true][y_true][floor_est][x_est][y_est][error][floor_error]
"""

import requests
import json
import sys, os
import numpy as np


"""
This table converts building
codes to building strings.
"""

BuildingCodeToStr = {
	-1: "Building",
	31: "SB",
	4: "AM",
	64: "IS",
	65: "KI"
}

"""
This object will represent an IBeacon throughout
the duration of a test case. It will hold all of
the rssi values this beacon transmitted during a
test case along with multiple different averages.
"""

class IBeacon:
	
	def __init__(self): 
		self.major = None
		self.minor = None
		self.rssis = None
		self.building = None
		self.floor = None
		self.x = None
		self.y = None
		self.dbm_sum = None
		self.mw_sum = None
		self.dbm_avg = None
		self.mw_avg = None
		self.mw_to_dbm_avg = None
		
	def setBeacon(self, building, floor, x, y):
		self.building = BuildingCodeToStr[building]
		self.floor = floor
		self.x = x;
		self.y = y;
	
	"""
	This function will initialize a beacon from
	a single database record. It will be called
	immediately after a call to IBeacon(). This 
	function can only be called if the beacon
	position was found in the DB.
	"""
	
	def setBeaconFromRecord(self, record, beacon_positions):
		self.major = str(record["beacon_major"])
		self.minor = str(record["beacon_minor"])
		self.key = self.major + self.minor
		self.building = beacon_positions[self.key].building
		self.floor = beacon_positions[self.key].floor
		self.x = beacon_positions[self.key].x
		self.y = beacon_positions[self.key].y
		self.rssis = []
		self.dbm_sum = 0
		self.mw_sum = 0
		self.dbm_avg = 0
		self.mw_avg = 0
		self.mw_to_dbm_avg = 0
		self.addRssi(record)
	
	"""
	This function will add an rssi to the beacon.
	It will also compute the different averages.
	"""
	
	def addRssi(self, record):
		rssi = record["rssi"]
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
This object will represent a single test case.
A test case is comprised of a user's testing
position (building, floor, x, y), the amount
of time the bluetooth scan was conducted,
and the list of unique beacons.
"""

class TestCase:

	def __init__(self, record, beacon_positions):
		self.beacon_positions = beacon_positions
		self.checked_beacon = {}
		self.checked_url = {}
		self.building = BuildingCodeToStr[record["building_id"]];
		self.floor_true = int(record["floor"]);
		self.x_true = float(record["x"]);
		self.y_true = float(record["y"]);
		self.scan_period = int(record["interval"]);
		self.test_id = record["testid"]
		self.beacons = []
		self.iteration = 0
		
		self.floor_est = 0
		self.x_est = 0.0
		self.y_est = 0.0
		self.error = 0.0
		self.floor_error = 0
		
		self.addRecord(record, beacon_positions);
	
	"""
	This function computes the url of the beacon
	position API based on the information in
	the record.
	"""
	
	def getBeaconLocUrl(self, record):
		url_str = "https://api.iitrtclab.com/beacons/"
		url_str += BuildingCodeToStr[record["building_id"]] + "/"
		url_str += str(record["floor"])
		return(url_str)
	
	"""
	This function will add a record to the test case.
	It will extract the beacon information from the
	record, and create a new beacon if it didn't
	already exist. The beacon position will be downloaded
	from BOSSA. If the beacon did exist, we will just
	add the rssi to the list of rssis in the beacon.
	"""
	
	def addRecord(self, record, beacon_positions):
		key = str(record["beacon_major"]) + str(record["beacon_minor"])
		
		#If the key is not in the beacon position list,
		#we will have to acquire it from the DB.
		if(key not in beacon_positions):
		
			#Make sure it's worth downloading the beacon data
			url_str = self.getBeaconLocUrl(record)
			if(url_str in self.checked_url):
				return;
			self.checked_url[url_str] = True
			
			#Download all beacons from a floor
			payload = {
				'major': record["beacon_major"],
				'minor': record["beacon_minor"]
			}
			json_records = requests.get(url_str, params=payload)  
			pos_records = json.loads(json_records.content.decode('utf-8'))
			
			#Iterate over all beacon from a floor and add to beacon positions
			for pos in pos_records:
				beacon = IBeacon()
				beacon.setBeacon(pos["building_id"], pos["floor"], pos["x"], pos["y"])
				beacon_positions[str(pos["major"])+str(pos["minor"])] = beacon
		
		#Add a beacon to the list of unique beacons OR
		#add an rssi to an existing beacon
		if(key in beacon_positions):
			if(key not in self.checked_beacon):
				beacon = IBeacon()
				beacon.setBeaconFromRecord(record, beacon_positions)
				self.beacons.append(beacon)
				self.checked_beacon[key] = beacon
			else:
				self.checked_beacon[key].addRssi(record)

				
	"""
	Sort beacons by mw_to_dbm_avg
	"""
	
	def avgMwToDbm(self, beacon):
		return beacon.mw_to_dbm_avg
			
	"""
	This function will acquire the beacons whose
	average rssi was computed by averaging power
	and then converting from power to dbm.
	"""
	
	def getNearestBeaconsAvgMwToDbm(self, n=3):
		self.beacons.sort(reverse = True, key = self.avgMwToDbm)
		subset = self.beacons[0:n]
		
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
	
	"""
	This function will set the results of a test.
	"""
	
	def setTestResults(self, x_est, y_est, floor_est):
		self.x_est = x_est
		self.y_est = y_est
		self.floor_est = floor_est
		self.error = ((self.x_true - self.x_est)**2 + (self.y_true - self.y_est)**2)**.5
		self.floor_error = abs(floor_est - self.floor_true)
			
	"""
	This will initialize an iteration
	of all beacons over this object.
	"""
	def __iter__(self):
		self.iteration = iter(self.beacons)
		return self
	
	
	"""
	This will acquire the next beacon
	in an iteration.
	"""
	
	def __next__(self):
		return self.iteration.next()
		
	
	def __str__(self):
		string = ""
		string += "Test ID: " + str(self.test_id) + "\n"
		string += "\tBuilding: " + str(self.building) + "\n"
		string += "\tFloor: " + str(self.floor_true) + "\n"
		string += "\tPosition: (" + str(self.x_true) + ", " + str(self.y_true) + ")\n"
		string += "\tScan Duration: " + str(self.scan_period) + "\n"
		string += "\tBEACONS:\n"
		for beacon in self.beacons:
			string += str(beacon)
		string += "\n"
		string += "Floor Estimate: " + str(self.floor_est) + "\n"
		string += "Position Estimate: (" + str(self.x_est) + ", " + str(self.y_est) + ")\n"
		string += "Error: " + str(self.error) + "\n"
		
		return string


"""
This object will be a list of test cases.
We will run the algorithms on each test
case in this object.
"""

class TestCases:
	
	def __init__(self):
		self.beacon_positions = {}
		self.test_ids = {}
		self.test_cases = []
		self.iteration = 0
		self.acquireAllRecords()
	
	"""
	This function acquires all test cases from
	the database. It will partition the test
	data based on testid. 
	
	In other words, we will create a list of test cases. 
	Each element of this list will be a test case. Each 
	test case is a set of records from the database who
	have the same testid.
	"""
	def acquireAllRecords(self):
		self.beacon_positions = {}
		self.test_ids = {}
		self.test_cases = []
		
		url_str = "https://api.iitrtclab.com/test"
		json_records = requests.get(url_str, "")
		records = json.loads(json_records.content.decode('utf-8'))
		self.partitionRecords(records);
	
	"""
	This function will convert the list of test records
	into a list of test cases. It will also build a list
	of beacon positions.
	"""

	def partitionRecords(self, records):
		for record in records:
			if(record["testid"] not in self.test_ids):
				test_case = TestCase(record, self.beacon_positions)
				self.test_cases.append(test_case)
				self.test_ids[record["testid"]] = test_case
			else:
				self.test_ids[record["testid"]].addRecord(record, self.beacon_positions)
				
	"""
	This function initializes the
	iterator.
	"""
	def __iter__(self):
		self.iteration = iter(self.test_cases)
		return self
	
	"""
	This function iterates over all of
	the test cases. Upon each iteration,
	it will return a TestCase object.
	"""
	def __next__(self): 
		return self.iteration.__next__()
		
	"""
	This function will print out all of
	the test cases
	"""
	
	def __str__(self):
		string = ""
		for test_case in self.test_cases:
			string += str(test_case) + "\n"
		return string 
	
	"""
	This function will convert the test case analysis
	into a CSV file.
	"""
		
	def toCsv(self, output="testresults.csv"):
		try:
			file = open(output, "w")
			string = "testid,beacon_major,beacon_minor,b_building,b_floor,b_x,b_y,rssi,duration,building,floor_true,x_true,y_true,floor_est,x_est,y_est,error,floor_error\n"
			for test_case in self.test_cases:
				for beacon in test_case.beacons:
					for rssi in beacon.rssis:
						string += "\"" + str(test_case.test_id) + "\"" + ","
						string += str(beacon.major) + ","
						string += str(beacon.minor) + ","
						string += "\"" + str(beacon.building) + "\"" + ","
						string += str(beacon.floor) + ","
						string += str(beacon.x) + ","
						string += str(beacon.y) + ","
						string += str(rssi) + ","
						string += str(test_case.scan_period) + ","
						string += "\"" + str(test_case.building) + "\"" + ","
						string += str(test_case.floor_true) + ","
						string += str(test_case.x_true) + ","
						string += str(test_case.y_true) + ","
						string += str(test_case.floor_est) + ","
						string += str(test_case.x_est) + ","
						string += str(test_case.y_est) + ","
						string += str(test_case.error) + ","
						string += str(test_case.floor_error)
						string += "\n"
			
			file.write(string)		
			file.close()
		except:
			print("There was a problem with creating the csv")

					
					