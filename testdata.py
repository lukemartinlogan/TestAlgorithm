
"""
This file acquires test cases from the database and
puts them into a meaningful format. 

table schemas:
	test data table 1: 	[testid][beacon_major][beacon_minor][building_id][floor][x][y][rssi][interval][id][timestamp]
	test data table 2:	[testid][beacon_major][beacon_minor][building_id][t_floor][t_x][t_y][bt_floor][bt_x][bt_y][rssi][interval][id][timestamp]
	beacon table:	 	[beacon_id][major][minor][building_id][floor][x][y][loc_id][temperature][humidity][updatetimestamp]

csv1 schema: [major][minor][rssi][testid][t_floor][t_x][t_y][bt_floor][bt_x][bt_Y][deployid][watt][proximity]
output csv schema: [testid][duration][top_n_beacons][algorithm][building][floor_true][x_true][y_true][floor_est][x_est][y_est][error][floor_error]

NOTE: for test data table 1, beacon positions are not stored with the record itself. So floor, x, and y
represent the testing device's position, not the bluetooth beacon position.

NOTE: test data table 2 has not been created when this file was created. I'm assuming that
the schema for this table will be exactly as written above.
"""

import requests
import json
import sys, os
import numpy as np
import csv

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

def GetBuildingName(code):
	try:
		return BuildingCodeToStr[code]
	except KeyError:
		return "Building"

"""
--------------------------------------------------
This object will represent an IBeacon throughout
the duration of a test case. It will hold all of
the rssi values this beacon transmitted during a
test case along with multiple different averages.
--------------------------------------------------
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
	
	"""
	This function initializes a beacon whose
	rssis will not be considered.
	"""
	
	def initBeacon(self, building, floor, x, y):
		self.building = GetBuildingName(building)
		self.floor = floor
		self.x = x;
		self.y = y;
	
	"""
	This function will initialize a beacon from
	a record from test table 1. It will be called
	immediately after a call to IBeacon(). This 
	function can only be called if the beacon
	position was found in the DB.
	"""
	
	def initBeaconFromRecord1(self, record, beacon_positions):
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
		
	"""
	This function will initialize a beacon from
	a record from test table 2. It will be called
	immediately after a call to IBeacon().
	"""
	
	def initBeaconFromRecord2(self, record):
		self.major = str(record["beacon_major"])
		self.minor = str(record["beacon_minor"])
		self.key = self.major + self.minor
		self.building = GetBuilding(record["building_id"])
		self.floor = record["bt_floor"]
		self.x = record["bt_x"]
		self.y = record["bt_y"]
		self.rssis = []
		self.dbm_sum = 0
		self.mw_sum = 0
		self.dbm_avg = 0
		self.mw_avg = 0
		self.mw_to_dbm_avg = 0
	
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
---------------------------------------------
This object will represent a single test case.
A test case is comprised of a user's testing
position (building, floor, x, y), the amount
of time the bluetooth scan was conducted,
and the list of unique beacons.
---------------------------------------------
"""

class TestCase:

	def __init__(self, record, beacon_positions=None):
		if(beacon_positions is not None):
			self.initTestCase1(record, beacon_positions)
		else:
			self.initTestCase2(record)
	
	"""
	Initialize test case from record with same schema
	as test data table 1.
	"""
	def initTestCase1(self, record, beacon_positions):
		self.beacon_positions = beacon_positions
		self.checked_beacon = {}
		self.checked_url = {}
		self.algorithm = 1
		self.building = GetBuildingName(record["building_id"]);
		self.floor_true = int(record["floor"]);
		self.x_true = float(record["x"]);
		self.y_true = float(record["y"]);
		self.scan_period = int(record["interval"]);
		self.test_id = record["testid"]
		self.beacons = []
		self.iteration = 0
		self.top_n = 3
		
		self.floor_est = 0
		self.x_est = 0.0
		self.y_est = 0.0
		self.error = 0.0
		self.floor_error = 0
		
	"""
	Initialize test case from record with same schema
	as test data table 2
	"""
	
	def initTestCase2(self, record):
		self.checked_beacon = {}
		self.checked_url = {}
		self.algorithm = 1
		self.building = GetBuildingName(record["building_id"]);
		self.floor_true = int(record["t_floor"]);
		self.x_true = float(record["t_x"]);
		self.y_true = float(record["t_y"]);
		self.scan_period = int(record["interval"]);
		self.test_id = record["testid"]
		self.beacons = []
		self.iteration = 0
		self.top_n = 3
		
		self.floor_est = 0
		self.x_est = 0.0
		self.y_est = 0.0
		self.error = 0.0
		self.floor_error = 0
		
	"""
	This function sets the algorithm being used
	in this test case.
	"""
	
	def setAlgorithm(self, id):
		self.algorithm = id
	
	"""
	This function computes the url of the beacon
	position API based on the information in
	the record.
	"""
	
	def getBeaconLocUrl(self, record):
		url_str = "https://api.iitrtclab.com/beacons/"
		url_str += GetBuildingName(record["building_id"]) + "/"
		url_str += str(record["floor"])
		return(url_str)
	
	"""
	This function will add a record from test data table 1
	to the test case. It will extract the beacon information 
	from the record, and create a new beacon if it didn't
	already exist. The beacon position will be downloaded
	from BOSSA. If the beacon did exist, we will just
	add the rssi to the list of rssis in the beacon.
	"""
	
	def addRecord1(self, record):
		key = str(record["beacon_major"]) + str(record["beacon_minor"])
		
		#If the key is not in the beacon position list,
		#we will have to acquire it from the DB.
		if(key not in self.beacon_positions):
		
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
			
			#Iterate over all beacons from the floor and add to beacon positions
			for pos in pos_records:
				beacon = IBeacon()
				beacon.initBeacon(pos["building_id"], pos["floor"], pos["x"], pos["y"])
				self.beacon_positions[str(pos["major"])+str(pos["minor"])] = beacon
		
		#Add a beacon to the list of unique beacons OR
		#add an rssi to an existing beacon
		if(key in self.beacon_positions):
			if(key not in self.checked_beacon):
				beacon = IBeacon()
				beacon.initBeaconFromRecord1(record, self.beacon_positions)
				self.beacons.append(beacon)
				self.checked_beacon[key] = beacon
			self.checked_beacon[key].addRssi(record)

	
	"""
	This function will add a record from test data table 2
	to the test case. It will extract the beacon information
	from the record, and create a new beacon if it didn't
	already exist. The beacon position is included with
	the record.
	"""
	
	def addRecord2(self, record):
		key = str(record["beacon_major"]) + str(record["beacon_minor"])
				
		#Add a beacon to the list of unique beacons OR
		#add an rssi to an existing beacon
		if(key not in self.checked_beacon):
			beacon = IBeacon()
			beacon.initBeaconFromRecord2(record)
			self.beacons.append(beacon)
			self.checked_beacon[key] = beacon
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
		self.top_n = n
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
		string += "\tTop N Beacons: " + str(self.top_n) + "\n"
		string += "\tBEACONS:\n"
		for beacon in self.beacons:
			string += str(beacon)
		string += "\n"
		string += "Floor Estimate: " + str(self.floor_est) + "\n"
		string += "Position Estimate: (" + str(self.x_est) + ", " + str(self.y_est) + ")\n"
		string += "Error: " + str(self.error) + "\n"
		
		return string


"""
------------------------------------------
This object will be a list of test cases.
We will run the algorithms on each test
case in this object.
------------------------------------------
"""

class TestCases:
	
	def __init__(self):
		self.beacon_positions = {}
		self.test_ids = {}
		self.test_cases = []
		self.iteration = 0
		self.csvOut = "testresults.csv"
	
	"""
	This function acquires all test cases from
	the database. It will partition the test
	data based on testid. It assumes that the
	table schema is test data table 1.
	
	In other words, we will create a list of test cases. 
	Each element of this list will be a test case. Each 
	test case is a set of records from the database who
	have the same testid.
	"""
	
	def downloadTestTable1(self):
		self.beacon_positions = {}
		self.test_ids = {}
		self.test_cases = []
		
		url_str = "https://api.iitrtclab.com/test"
		json_records = requests.get(url_str, "")
		records = json.loads(json_records.content.decode('utf-8'))
		self.partitionTestTable1(records);
		
	"""
	This function will convert the list of test records
	into a list of test cases. It will also build a list
	of beacon positions.
	
	This version assumes that the beacon positions ARE NOT stored
	with the test file and will download them from the database.
	"""

	def partitionTestTable1(self, records):
		for record in records:
			if(record["testid"] not in self.test_ids):
				test_case = TestCase(record, self.beacon_positions)
				self.test_cases.append(test_case)
				self.test_ids[record["testid"]] = test_case
			self.test_ids[record["testid"]].addRecord1(record)
		
	"""
	This function acquires the test data from a csv1 file and converts it
	to a record with the same form as test data table 2.
	
	[major][minor][rssi][testid][t_floor][t_x][t_y][bt_floor][bt_x][bt_Y][deployid][watt][proximity] ->
	[testid][beacon_major][beacon_minor][building_id][t_floor][t_x][t_y][bt_floor][bt_x][bt_y][rssi][interval][id][timestamp]
	
	NOTE: the csv file of type 1 does NOT include building id, record id (id), or timestamp. The
	scan interval (interval) is 10 seconds. The csv1 file also includes some info we do not need:
	(watt and proximity).
	"""
	
	def loadCsv1(self, url):
		file = open(url)
		reader = csv.DictReader(file);
		
		records = []
		for r in reader:
			record = {}
			record["testid"] = r["testid"]
			record["beacon_major"] = int(r["major"])
			record["beacon_minor"] = int(r["minor"])
			record["building_id"] = -1
			record["t_floor"] = int(r["t_floor"])
			record["t_x"] = float(r["t_x"])
			record["t_y"] = float(r["t_y"])
			record["bt_floor"] = int(r["bt_floor"])
			record["bt_x"] = float(r["bt_x"])
			record["bt_y"] = float(r["bt_Y"])
			record["rssi"] = float(r["rssi"])
			record["interval"] = 10
			record["id"] = -1
			record["timestamp"] = 0
			records.append(record)
		
		self.partitionTestTable2(records)
		
	"""
	This function imports a folder containing only csv1 files.
	"""
	
	def loadCsv1Folder(self, url):
		files = os.listdir(url)
		for file in files:
			self.loadCsv1(url + "/" + file)
	
	
	"""
	This function will convert the list of test records
	into a list of test cases.
	
	This version assumes that the beacon positions ARE stored
	with the test file and will download them from the database.
	"""
	
	def partitionTestTable2(self, records):
		for record in records:
			if(record["testid"] not in self.test_ids):
				test_case = TestCase(record)
				self.test_cases.append(test_case)
				self.test_ids[record["testid"]] = test_case
			self.test_ids[record["testid"]].addRecord2(record)
	
	
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
	Set the csv output location
	"""
	
	def setCsvUrl(self, output):
		self.csvOut = output
		
		
	"""
	This function will convert the test case data into
	a CSV file.
	
	Output CSV schema 2
	"""
	
	def testDataToCsv(self, filename):
		output = open(filename, "w")
		
		string = "testid,bt_major,bt_minor,bt_x,bt_y,building_id,t_floor,t_x,t_y,bt_floor,rssi,interval"
		try:
			for test_case in self.test_cases:
				for(
				string += "\"" + str(test_case.test_id) + "\"" + ","
				string += str(test_case.bt_major) + ","
				string += str(test_case.bt_minor) + ","
				string += str(test_case.bt_major) + ","
				string += str(test_case.bt_major) + ","
				string += "\"" + str(test_case.building) + "\"" + ","
				string += str(test_case.floor_true) + ","
				string += str(test_case.x_true) + ","
				string += str(test_case.y_true) + ","
				string += str(test_case.floor_est) + ","
				string += str(test_case.x_est) + ","
				string += str(test_case.y_est) + ","
				string += "\n"
			
			output.write(string)
			output.close()
		except:
			print("There was a problem with creating the csv")
	
	"""
	This function will convert the test case analysis
	into a CSV file.
	"""
		
	def toCsv(self, output=None):
	
		if(output is None):
			output = self.csvOut
	
		try:
			string = ""
			if(not os.path.isfile(output)):
				string = "testid,duration,top_n_beacons,algorithm,building,floor_true,x_true,y_true,floor_est,x_est,y_est,error,floor_error\n"
			file = open(output, "a")
			
			for test_case in self.test_cases:
				string += "\"" + str(test_case.test_id) + "\"" + ","
				string += str(test_case.scan_period) + ","
				string += str(test_case.top_n) + ","
				string += str(test_case.algorithm) + ","
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

					













					