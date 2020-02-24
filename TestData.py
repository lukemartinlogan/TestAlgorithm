
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
import pandas as pd
import ssl



BuildingCodeToStr = {
	-1: "Building",
	31: "SB",
	4: "AM",
	64: "IS",
	65: "KI"
}

BuildingStrToCode = {
	"Building" : -1,
	"SB" : 31,
	"AM": 4,
	"IS": 64,
	"KI" : 65
}

def GetBuildingName(code):
	try:
		return BuildingCodeToStr[code]
	except KeyError:
		return "Building"
		
def download_test_data1(out = "Datasets/full_database.csv"):
	
		"""
		This function will download test data from the "test application"
		database and save it as a CSV file.
		
		The "test application" database has the following schema:
		[testid][beacon_major][beacon_minor][building_id][floor][x][y][rssi][interval][id][timestamp]
		
		We will save this data to a CSV file with the following column names:
		[testid][b_major][b_minor][b_floor][b_x][b_y][t_building][t_floor][t_x][t_y][rssi][interval][timestamp]
		
		Inputs:
			out: The location to save the csv to
		Return:
			This function will save a CSV file at the location "out"
		"""
		
		ssl._create_default_https_context = ssl._create_unverified_context
		
		#Download the test data
		print("Downloading test data")
		tests = pd.read_json("https://api.iitrtclab.com/test")
		tests = tests.rename(
			columns={
				"x" : "t_x",
				"y" : "t_y",
				"building_id" : "t_building",
				"floor" : "t_floor",
				"beacon_major" : "b_major",
				"beacon_minor" : "b_minor"
			}
		)
		tests = tests.drop("id", axis=1)
		tests = tests[tests["testid"] != "FAKE_TEST"]
		tests = tests[tests["testid"] != "FAKE_TEST_2"]
		tests = tests[tests["testid"] != "FAKE_TEST_3"]
		
		#Find the unique major/minors of beacons
		print("Unique major/minor")
		bids = tests[["b_major", "b_minor"]].drop_duplicates()
		
		#Find the unique buildings the beacons are in
		print("Unique buildings")
		buildings = tests["t_building"].drop_duplicates()
		
		#Get the beacon data for each building
		print("Getting beacon data")
		blocs = pd.DataFrame()
		for building in buildings:
			name = GetBuildingName(building)
			if name == "Building":
				continue
			
			bloc = pd.read_json("https://api.iitrtclab.com/beacons/" + name)
			blocs = blocs.append(bloc)
		
		#We don't need humidity, loc_id, building, timestamp, or temperature
		blocs = blocs.drop(["humidity", "loc_id", "building_id", "updatetimestamp", "temperature"], axis=1)
		
		#We need to rename x, y, and floor in this table
		blocs = blocs.rename(
			columns={
				"major" : "b_major",
				"minor" : "b_minor",
				"x" : "b_x",
				"y" : "b_y",
				"floor" : "b_floor"
			}
		)
		
		#Left join the beacon data on the test data table using (major, minor)
		tests = tests.merge(
			right = blocs,
			how = "left",
			on = ["b_major", "b_minor"]
		)
		
		#Save this dataframe as a CSV
		tests = tests.dropna(axis=0, subset=["b_x", "b_y"])
		tests.to_csv(out, index=False)
		
def download_beacons(loc="https://api.iitrtclab.com/beacons", out = "Datasets/beacons.csv"):
	
	"""
	Download and store the beacon information
	"""
	
	ssl._create_default_https_context = ssl._create_unverified_context
	
	#Get the beacon data for each building
	print("Getting beacon data")
	blocs = pd.read_json("https://api.iitrtclab.com/beacons")
	
	#We don't need humidity, loc_id, building, timestamp, or temperature
	blocs = blocs.drop(["humidity", "loc_id", "updatetimestamp", "temperature"], axis=1)
	
	#We need to rename x, y, and floor in this table
	blocs = blocs.rename(
		columns={
			"beacon_id" : "b_id",
			"major" : "b_major",
			"minor" : "b_minor",
			"x" : "b_x",
			"y" : "b_y",
			"floor" : "b_floor",
			"building_id" : "b_building"
		}
	)
	
	#Save this dataframe as a CSV
	blocs.to_csv(out, index=False)

def download_gateways(loc="https://api.iitrtclab.com/gateways", out = "Datasets/gateways.csv"):
	
	"""
	Download and store the red bear information
	"""
	
	ssl._create_default_https_context = ssl._create_unverified_context
	
	#Get the beacon data for each building
	print("Getting red bear data")
	gateways = pd.read_json(loc) 
	
	#We don't need humidity, loc_id, building, timestamp, or temperature
	gateways = gateways.drop(["charged", "lastseen"], axis=1)
	
	#We need to rename x, y, and floor in this table
	gateways = gateways.rename(
		columns={
			"gateway_id" : "g_id",
			"major" : "g_major",
			"minor" : "g_minor",
			"x" : "g_x",
			"y" : "g_y",
			"floor" : "g_floor",
			"building_id" : "g_building"
		}
	)
	
	#Save this dataframe as a CSV
	gateways.to_csv(out, index=False)



