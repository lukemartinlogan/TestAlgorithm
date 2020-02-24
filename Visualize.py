
import pandas as pd
from TestData import *
import datetime

def get_img_path(building, floor, portrait=False):

	"""
	This function will acquire the path to the map file being
	queried. This function assumes that the set of maps is
	in the current working directory.

	Inputs:
		building: the building we are finding a map for
		floor: the exact floor of this building we are finding a map of
		portrait: whether we are going to use the portrait (tall) or landscape (long) version of the map
	"""

	if portrait:
		return "./Maps/{}-{:02d}.html".format(building, floor)
	else:
		return "./Maps/{}-{:02d}-R.html".format(building, floor)

def view_test_positions(cases, building="SB", floor=1, top_n=3, portrait=False, days=None, save_path=None):

	"""
	Visualize the testing positions
	"""

	#Get the html we will be modifying
	img_file = open(get_img_path(building, floor, portrait))
	img = img_file.read()

	#Get the file with the map javascript data
	map_file = open("./Maps/map.js")
	map = map_file.read()
	img += map

	#Start the javascript
	img += "<script>\n"

	#Convert the portrait boolean to Javascript boolean
	if portrait:
		portrait = "true"
	else:
		portrait = "false"

	#Get building code
	code = BuildingStrToCode[building]

	#Draw test positions
	for case in cases.test_cases.values():
		img += "render_test_pos("
		img += "\"" + str(case.testid) + "\"" + ","
		img += str(case.x_true) + ","
		img += str(case.y_true) + ","
		img += portrait
		img += ")\n"

	#Draw beacon positions
	beacons = pd.read_csv("Datasets/beacons.csv")
	beacons = beacons[
		(beacons["b_building"] == code) &
		(beacons["b_floor"] == floor)
	]
	for idx, b in beacons.iterrows():
		img += "render_beacon("
		img += str(b["b_major"]) + ","
		img += str(b["b_minor"]) + ","
		img += "\"" + str(BuildingCodeToStr[b["b_building"]]) + "\"" + ","
		img += str(b["b_floor"]) + ","
		img += str(b["b_x"]) + ","
		img += str(b["b_y"]) + ","
		img += "0" + ","
		img += portrait
		img += ")\n"
		
	#Draw gateway positions
	"""
	gateways = pd.read_csv("Datasets/gateways.csv")
	gateways = gateways[
		(gateways["g_building"] == code) &
		(gateways["g_floor"] == floor)
	]
	for idx, g in gateways.iterrows():
		img += "render_gateway("
		img += str(g["g_major"]) + ","
		img += str(g["g_minor"]) + ","
		img += "\"" + str(BuildingCodeToStr[g["g_building"]]) + "\"" + ","
		img += str(g["g_floor"]) + ","
		img += str(g["g_x"]) + ","
		img += str(g["g_y"]) + ","
		img += portrait
		img += ")\n"
	"""
	
	#End the javascript
	img += "</script>\n"

	#End the html file
	img += "</html>"
	save = open(save_path, "w")
	save.write(img)
	return

def view_tests(
	results=None, building="SB", floor=1, days=None, interval=5,
	loc_alg=2, floor_algorithm=2, bin_strategy=1, top_n=3,
	num_results=10, xy_error=0, portrait=False, save_path=None
):

	"""
	View all tests over a certain period of time.
	
	It will display the tester's position in green and the estimated positions
	in purple.

	Inputs:
		results: 			a pandas dataframe consisting of all test case results (from TestAlgorithm)
		database:			a pandas dataframe of the raw test data (including beacon positions)
		building: 			the building the tests occurred in
		floor: 				the floor of the building the tests occurred on
		days: 				the range of days at which tests were made (Year, Month, Day)
		loc_alg: 			the algorithm used to estimate xy position
		floor_algorithm: 	the algorithm used to estimate the floor
		bin_strategy:		the binning strategy used for converting RSSI to distance
		top_n: 				the number of beacons factored when estimating xy position
		num_results: 		the number of results to display from the dataframe
		xy_error: 			display only error greater than or equal to this value
		portrait:			whether to use the portrait or landscape form of the building map
		save_path: 			the path to save the image to
	"""

	#Get the html we will be modifying
	img_file = open(get_img_path(building, floor, portrait))
	img = img_file.read()

	#Get the file with the map javascript data
	map_file = open("./Maps/map.js")
	map = map_file.read()
	img += map

	#Start the javascript
	img += "<script>\n"

	#Convert the portrait boolean to Javascript boolean
	if portrait:
		portrait = "true"
	else:
		portrait = "false"

	#Get building code
	code = BuildingStrToCode[building]

	if results is not None:
		#Get the result we will displaying
		results = results[
			(results["building_true"] == code) &
			(results["floor_true"] == floor) &
			(results["interval"] == interval) &
			(results["loc_alg"] == loc_alg) &
			(results["floor_alg"] == floor_algorithm) &
			(results["bin_strat"] == bin_strategy) &
			(results["xy_error"] >= xy_error) &
			(results["top_n"] == top_n)
		]

		if days is not None:
			pd.to_datetime(results["timestamp"])
			day_start = str(datetime.date(days[0][0], days[0][1], days[0][2]))
			day_end = str(datetime.date(days[1][0], days[1][1], days[1][2]))
			results = results[(results['timestamp'] >= day_start) & (results['timestamp'] <= day_end)]

		#Write the test cases to the screen
		results = results.head(num_results)
		for idx, res in results.iterrows():
			img += "render_test_case("
			img += "\"" + res["testid"] + "\"" + ","
			img += str(res["x_true"]) + ","
			img += str(res["y_true"]) + ","
			img += str(res["x_est"]) + ","
			img += str(res["y_est"]) + ","
			img += str(res["xy_error"]) + ","
			img += "\"" + str(res["timestamp"]) + "\"" + ","
			img += portrait
			img += ")\n"
	
	#Draw beacon positions
	beacons = pd.read_csv("Datasets/beacons.csv")
	beacons = beacons[
		(beacons["b_building"] == code) &
		(beacons["b_floor"] == floor)
	]
	for idx, b in beacons.iterrows():
		img += "render_beacon("
		img += str(b["b_major"]) + ","
		img += str(b["b_minor"]) + ","
		img += "\"" + str(BuildingCodeToStr[b["b_building"]]) + "\"" + ","
		img += str(b["b_floor"]) + ","
		img += str(b["b_x"]) + ","
		img += str(b["b_y"]) + ","
		img += "0" + ","
		img += portrait
		img += ")\n"
	
	#End the javascript
	img += "</script>\n"

	#End the html file
	img += "</html>"
	save = open(save_path, "w")
	save.write(img)

def view_test_cases(cases, building="SB", floor=1, top_n=3, days=None, portrait=False, save_path=None):

	"""
	View a specific subset of tests.
	"""

	#Get the html we will be modifying
	img_file = open(get_img_path(building, floor, portrait))
	img = img_file.read()

	#Get the file with the map javascript data
	map_file = open("./Maps/map.js")
	map = map_file.read()
	img += map

	#Start the javascript
	img += "<script>\n"

	#Convert the portrait boolean to Javascript boolean
	if portrait:
		portrait = "true"
	else:
		portrait = "false"

	#Get building code
	code = BuildingStrToCode[building]

	#Draw beacon positions
	beacons = pd.read_csv("Datasets/beacons.csv")
	beacons = beacons[
		(beacons["b_building"] == code) &
		(beacons["b_floor"] == floor)
	]
	for idx, b in beacons.iterrows():
		img += "render_beacon("
		img += str(b["b_major"]) + ","
		img += str(b["b_minor"]) + ","
		img += "\"" + str(BuildingCodeToStr[b["b_building"]]) + "\"" + ","
		img += str(b["b_floor"]) + ","
		img += str(b["b_x"]) + ","
		img += str(b["b_y"]) + ","
		img += "0" + ","
		img += portrait
		img += ")\n"
	
	#Draw test cases
	for case in cases.test_cases.values():
		img += "render_test_case("
		img += "\"" + str(case.testid) + "\"" + ","
		img += str(case.x_true) + ","
		img += str(case.y_true) + ","
		img += str(case.x_est) + ","
		img += str(case.y_est) + ","
		img += str(case.xy_error) + ","
		img += "\"" + str(case.timestamp) + "\"" + ","
		img += portrait
		img += ")\n"

	#End the javascript
	img += "</script>\n"

	#End the html file
	img += "</html>"
	save = open(save_path, "w")
	save.write(img)
	return
