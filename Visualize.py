
import pandas as pd
from TestData import *
import datetime


def load_results(path):

	"""
	This function will load the results of the test cases
	into a pandas dataframe.
	
	Inputs:
		path: the location of the test data results from TestAlgorithm.py
	Return:
		A pandas dataframe of test results
	"""

	return pd.read_csv(path, header=0)

	
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
	
	
def view_tests(
	df, tests=None, building="SB", floor=2, days=None, 
	loc_algorithm=2, floor_algorithm=1, bin_strategy=1, top_n=3,
	results=(0, 10), portrait=False, save_path=None
):
	
	"""
	This function displays the test data from a certain testing day on
	a map of the floor tested on.
	
	It will display the tester's position in green and the estimated positions
	in purple.
	
	Inputs:
		df: 				a pandas dataframe consisting of all test case results (from TestAlgorithm)
		tests:				a pandas dataframe of the test data (including beacon positions)
		building: 			the building the tests occurred in
		floor: 				the floor of the building the tests occurred on
		days: 				the range of days at which tests were made (Year, Month, Day)
		loc_algorithm: 		the algorithm used to estimate xy position
		floor_algorithm: 	the algorithm used to estimate the floor
		bin_strategy:		the binning strategy used for converting RSSI to distance
		top_n: 				the number of beacons factored when estimating xy position
		results: 			the range of results to display from the dataframe
		portrait:			whether to use the portrait or landscape form of the building map
		save_path: 			the path to save the image to
	"""
	
	#Get the html we will be modifying
	img_file = open(get_img_path(building, floor, portrait))
	img = img_file.read()
	
	#Get the data we will displaying
	code = BuildingStrToCode[building]
	df = df[
		(df["building_true"] == code) & 
		(df["floor_true"] == floor) & 
		(df["interval"] == 5) & 
		(df["loc_alg"] == loc_algorithm) &
		(df["floor_alg"] == floor_algorithm) &
		(df["bin_strat"] == bin_strategy) &
		(df["top_n"] == top_n)
	]
	
	if days is not None:
		pd.to_datetime(df["timestamp"])
		day_start = str(datetime.date(days[0][0], days[0][1], days[0][2]))
		day_end = str(datetime.date(days[1][0], days[1][1], days[1][2]))
		df = df[(df['timestamp'] >= day_start) & (df['timestamp'] <= day_end)]
	
	#Make sure we select a range of results within our query
	if results is None:
		results = (0, len(df) - 1)
	elif results[1] > len(df):
		results = (results[0], len(df)-1)
	print(results)
		
	#Convert the portrait boolean to a string
	if portrait:
		portrait = "true"
	else:
		portrait = "false"
	
	#Get the file with the map javascript data
	map_file = open("./Maps/map.js")
	map = map_file.read()
	img += map
	
	#Start the javascript
	img += "<script>\n"
	
	#Write the test cases to the screen
	for i in range(results[0], results[1]+1):
		idx = df.index[i]
		img += "render_test_case("
		img += "\"" + df.loc[idx, "testid"] + "\"" + ","
		img += str(df.loc[idx, "x_true"]) + ","
		img += str(df.loc[idx, "y_true"]) + ","
		img += str(df.loc[idx, "x_est"]) + ","
		img += str(df.loc[idx, "y_est"]) + ","
		img += str(df.loc[idx, "xy_error"]) + ","
		img += portrait
		img += ")\n"
	
	#Display bluetooth beacons on floor
	
	
	#End the javascript
	img += "</script>\n"
	
	#End the html file
	img += "</html>"
	save = open(save_path, "w")
	save.write(img)
