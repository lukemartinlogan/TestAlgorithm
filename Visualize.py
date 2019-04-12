
import pandas
import cv2

def load_results(path):
	return pandas.read_csv(path, header=0)
	
def get_img_path(building, floor, portrait=True):
	if portrait:
		return "./Maps/{}-{:02d}.html".format(building, floor)
	else:
		return "./Maps/{}-{:02d}-R.html".format(building, floor)
	
def view_tests(df, building="SB", floor=2, day=(2019, 3, 8), algorithm=2, bin=1, results=(0, 10), portrait=True, save_path=None):
	
	"""
	This function displays the test data from a certain testing day on
	a map of the floor tested on.
	
	It will display the tester's position in green and the estimated positions
	in purple.
	
	Inputs:
		df: a pandas dataframe consisting of all test cases
		building: the building the tests occurred in
		floor: the floor of the building the tests occurred on
		day: the day at which tests were made
		algorithm: the algorithm used to compute distances
		bin: the binning strategy used for computing distance
		results: the range of results to display from the dataframe
		save: the path to save the image to
	"""
	
	#Get the html we will be modifying
	img_file = open(get_img_path(building, floor, portrait))
	img = img_file.read()
	
	#Get the data we will displaying
	df = df[(df["building"] == building) & (df["floor_true"] == floor) & (df["duration"] == 5)]
	
	#Make sure we select a range of results within our query
	if results[1] > len(df):
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
	
	#Write the test cases to the screen
	img += "<script>\n"
	for i in range(results[0], results[1]+1):
		idx = df.index[i]
		img += "render_test_case("
		img += "\"" + df.loc[idx, "testid"] + "\"" + ","
		img += str(df.loc[idx, "x_true"]) + ","
		img += str(df.loc[idx, "y_true"]) + ","
		img += str(df.loc[idx, "x_est"]) + ","
		img += str(df.loc[idx, "y_est"]) + ","
		img += str(df.loc[idx, "error"]) + ","
		img += portrait
		img += ")\n"
	img += "</script>\n"
	
	#End the html file
	img += "</html>"
	save = open(save_path, "w")
	save.write(img)

def main():
	df = load_results("./testresults_NN.csv")
	#view_tests(df, building="SB", floor=1, save_path="./Visualizations/SB-01-results.html", portrait=True)
	view_tests(df, building="SB", floor=2, save_path="./Visualizations/SB-02-R-resultsNewBins.html", portrait=False, results=(0, 1000))
	
	df = load_results("./testresults_ON.csv")
	#view_tests(df, building="SB", floor=1, save_path="./Visualizations/SB-01-results.html", portrait=True)
	view_tests(df, building="SB", floor=2, save_path="./Visualizations/SB-02-R-resultsOldBins.html", portrait=False, results=(0, 1000))
	
if __name__ == "__main__":
	main()
	
