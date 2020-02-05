
"""
This file is responsible for removing invalid
test cases from the dataset taken from BOSSA.
"""

from TestData import *
from TestAlgorithm import *
from Visualize import *
from OptimizeBins import *
from AnalyzeAlgorithm import *
import pandas as pd

def test_algorithm():
	cases = TestCases(out="Datasets/results_to_clean.csv")
	
	print("Opening test cases - 5sec")
	cases.open_test_data(path="Datasets/full_database.csv", building="SB", interval=5)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 6, to_csv = True)
	
	print("Opening test cases - 10sec")
	cases.open_test_data(path="Datasets/full_database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 7, to_csv = True)

def visualize_erronous_points():
	df = load_results("Datasets/results.csv")
	
	days=[(2019, 1, 1), (2019, 4, 29)]
	
	"""
	view_tests(
		df, building="SB", loc_alg=2, floor=1, 
		days=days, 
		bin_strategy=6, save_path="Visualizations/SB01_5s_3.html", 
		interval=5,
		xy_error=7,
		results=(0, 100))
		
	view_tests(
		df, building="SB", loc_alg=2, floor=1, 
		days=days, 
		bin_strategy=6, save_path="Visualizations/SB01_5s_3.html", 
		interval=5,
		xy_error=7,
		results=(0, 100))
	"""
	view_tests(
		df, building="SB", loc_alg=2, floor=1, 
		days=days, 
		bin_strategy=3, save_path="Visualizations/SB01_10s_3.html", 
		interval=10,
		xy_error=0,
		results=(0, 100))
	"""
	view_tests(
		df, building="SB", loc_alg=2, floor=2, 
		days=days, 
		bin_strategy=3, save_path="Visualizations/SB02_10s_3.html", 
		interval=10, 
		xy_error=6,
		results=(0, 100))
		"""
	

def remove_test(df, testid): 
	return df[df["testid"] != testid]

def remove_invalid_tests():
	df = pd.read_csv("Datasets/full_database.csv")
	
	#Test points taken from improper positions (10s)
	df = remove_test(df, "Test30022")
	df = remove_test(df, "Test87030")
	df = remove_test(df, "Test37479")
	df = remove_test(df, "Test6781")
	df = remove_test(df, "Test78829")
	df = remove_test(df, "Test18722")
	df = remove_test(df, "Test60907")
	df = remove_test(df, "Test6310")
	df = remove_test(df, "Test50448")
	df = remove_test(df, "Test97265")
	df = remove_test(df, "Test56319")
	
	#Test points with large error (10s)
	df = remove_test(df, "Test8527")
	df = remove_test(df, "Test96257")
	df = remove_test(df, "Test5270")
	df = remove_test(df, "Test68121")
	
	#Test points taken from improper positions (5s)
	df = remove_test(df, "Test11881")
	df = remove_test(df, "Test5444")
	df = remove_test(df, "Test12599")
	df = remove_test(df, "Test96786")
	df = remove_test(df, "Test86088")
	df = remove_test(df, "Test73394")
	df = remove_test(df, "Test35814")
	df = remove_test(df, "Test53151")
	df = remove_test(df, "Test68842")
	df = remove_test(df, "Test52481")
	df = remove_test(df, "Test21017")
	df = remove_test(df, "Test15800")
	df = remove_test(df, "Test88279")
	
	#Test points taken from April 
	pd.to_datetime(df["timestamp"])
	day_start = str(datetime.date(2019, 4, 1))
	day_end = str(datetime.date(2019, 4, 5))
	df = df[(df['timestamp'] <= day_start) | (df['timestamp'] >= day_end)]
	
	df.to_csv("Datasets/database.csv", index=False)

def main():
	#test_algorithm()
	visualize_erronous_points()
	#remove_invalid_tests()

if __name__ == "__main__":
	main()

	
