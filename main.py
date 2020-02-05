
"""
This file contains a loose collection of test cases
I ran during the semester.
"""

from TestData import *
from TestAlgorithm import *
from Visualize import *
from OptimizeBins import *
from AnalyzeAlgorithm import *
from AnalyzeSignals import *
import pandas as pd

def main_download_database():
	download_test_data1(out="Datasets/full_database.csv")

def main_signal_stats():
	cases = TestCases()
	cases.open_test_data(database="Datasets/database.csv", building="SB", interval=5)
	ViewSignalStats(cases, hist_title="Signal Strengths in SB", hist_out="Visualizations/signal_strengths.png")
	
def main_optimize_bins():

	#Creating bin optimizer
	bins = BinOptimizer()
	
	#Open test data for 5sec interval
	print("Opening test cases - 5sec")
	cases = TestCases()
	cases.open_test_data(database="Datasets/database.csv", building="SB", interval=5)
	
	"""
	#Optimize - Fixed RSSI
	print("Optimizing Bins - Fixed RSSI - 5sec")
	bins.set_cases(cases)
	bins.optimize_fixed_rssi(
		bins=3, loc_alg=2, floor_alg=1, top_n=3,
		min_dist = 2, dist_width_range = (1,5),
		fix_dist_width = False,
		num_guesses = 100)
	print(bins)
	"""
	
	#Optimize - Varied
	print("Optimizing Bins - Varied - 5sec")
	bins.set_cases(cases)
	bins.optimize_full(
		bins=3, loc_alg=2, floor_alg=1, top_n=3,
		max_rssi = -60, rssi_width_range = (10,20),
		min_dist = 2, dist_width_range = (1,5),
		fix_rssi_width = True, fix_dist_width = False,
		num_guesses = 100)
	print(bins)
	
	#Open test data for 10sec interval
	print("Opening test cases - 10sec")
	cases = TestCases()
	cases.open_test_data(database="Datasets/database.csv", building="SB", interval=10)
	
	"""
	#Optimize - Fixed RSSI
	print("Optimizing Bins - Fixed RSSI - 10sec")
	bins.set_cases(cases)
	bins.optimize_fixed_rssi(
		bins=3, loc_alg=2, floor_alg=1, top_n=3,
		min_dist = 2, dist_width_range = (1,5),
		fix_dist_width = False,
		num_guesses = 100)
	print(bins)
	"""
	
	#Optimize - Varied
	print("Optimizing Bins - Varied - 10sec")
	bins.set_cases(cases)
	bins.optimize_full(
		bins=3, loc_alg=2, floor_alg=1, top_n=3,
		max_rssi = -60, rssi_width_range = (10,20),
		min_dist = 2, dist_width_range = (1,5),
		fix_rssi_width = True, fix_dist_width = False,
		num_guesses = 100)
	print(bins)

def main_test_alg():

	cases = TestCases(out="Datasets/results.csv", append=True)
	
	#Get the location estimates for the bin strategies (5s)
	print("Opening test cases -5sec")
	cases.open_test_data(database="Datasets/database.csv", building="SB", interval=5)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 3, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 8, to_csv = True)
	
	#Get the location estimates for the bin strategies (10s)
	print("Opening test cases -10sec")
	cases.open_test_data(database="Datasets/database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 3, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 9, to_csv = True)

def main_view_stats():
	df = pd.read_csv("Datasets/results.csv")
	
	print("Stats for 5s interval, strategy 3")
	ViewStats(
		bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df, 
		hist_title="Error Distribution SB (interval=5s, initial bins)", 
		hist_out="Visualizations/SB_err_hist_strat3_5s.png")
	
	print("Stats for 5s interval, strategy 8")
	ViewStats(
		bin_strat=8, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df, 
		hist_title="Error Distribution SB (interval=5s, optimized bins)", 
		hist_out="Visualizations/SB_err_hist_strat8_5s.png")
	
	print("Stats for 10s interval, strategy 3")
	ViewStats(
		bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df, 
		hist_title="Error Distribution SB interval=10s, initial bins)", 
		hist_out="Visualizations/SB_err_hist_strat3_10s.png")
	
	print("Stats for 10s interval, strategy 9")
	ViewStats(
		bin_strat=9, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df, 
		hist_title="Error Distribution SB (interval=10s, optimized bins)", 
		hist_out="Visualizations/SB_err_hist_strat9_10s.png")

def main_visualize():
	
	results = pd.read_csv("Datasets/results.csv")
	database = pd.read_csv("Datasets/database.csv")
	
	days = [(2019, 1, 1), (2019, 4, 29)]
	
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=3, save_path="Visualizations/SB01_5s_3.html", interval=5, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=8, save_path="Visualizations/SB01_5s_8.html", interval=5, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=3, save_path="Visualizations/SB02_5s_3.html", interval=5, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=6, save_path="Visualizations/SB02_5s_8.html", interval=5, num_results=100)
	
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=3, save_path="Visualizations/SB01_10s_3.html", interval=10, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=9, save_path="Visualizations/SB01_10s_9.html", interval=10, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=3, save_path="Visualizations/SB02_10s_3.html", interval=10, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=9, save_path="Visualizations/SB02_10s_9.html", interval=10, num_results=100)

def main_find_outliers():

	results = pd.read_csv("Datasets/results.csv")
	database = pd.read_csv("Datasets/database.csv")
	
	days=[(2019, 1, 1), (2019, 4, 29)]
	
	view_tests(
		results=results, database=database, building="SB", loc_alg=2, floor=1, 
		days=days, 
		bin_strategy=3, save_path="Visualizations/SB01_10s_3_outliers.html", 
		interval=10,
		xy_error=7,
		num_results=100)

def main_visualize_outlier():
	cases = TestCases()
	cases.open_test_cases(
		cases=["Test7045"], database="Datasets/database.csv", results="Datasets/results.csv",
		interval=10, loc_alg=2, floor_alg=1, bin_strategy=3, top_n=3
	)
	view_test_cases(cases,  building="SB", floor=1, top_n=3, portrait=False, save_path="Visualizations/outliers.html")
	return
	
def main():
	#main_signal_stats()
	#main_optimize_bins()
	#main_test_alg()
	#main_view_stats()
	#main_visualize()
	#main_find_outliers()
	main_visualize_outlier()

if __name__ == "__main__":
	main()

	
	
	
