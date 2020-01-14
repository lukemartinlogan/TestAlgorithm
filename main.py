
"""
This file contains a loose collection of test cases
I ran during the semester.
"""

from TestData import *
from TestAlgorithm import *
from Visualize import *
from OptimizeBins import *
from AnalyzeAlgorithm import *
import pandas as pd

def main_test_sim():
	
	#Open the test cases for a certain building
	print("Opening test cases")
	cases = TestCases(out="sim_results.csv")
	cases.open_test_data(path="SimulatedData.csv", building="SB")
	
	#Run the original bins over the new test data
	print("Testing original bin strategy")
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 2)
	cases.to_csv()
	
	#Run the new bins over the new test data
	print("Testing new bin strategy")
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 6)
	cases.to_csv()

def main_optimize_bins():

	#Creating bin optimizer
	bins = BinOptimizer()
	
	#Open the test cases for a certain building (interval=10sec)
	print("Opening test cases - 10sec")
	bins.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	
	#Genetic optimization
	print("Optimizing Bins")
	bins.optimize(loc_alg=2, floor_alg=1, top_n=3, num_bins=6, pop_size = 10, num_generations=10)
	print(bins)

def main_test_alg():

	#Get the location estimates for the two bin strategies
	print("Opening test cases -10sec")
	cases = TestCases(out="Datasets/results2.csv")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 2, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 7, to_csv = True)
	#cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 9, to_csv = True)
	
def main_compare_bins():
	CompareBinStrategies(
		bin_strat1=2, bin_strat2=7, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, 
		hist1_out="Visualizations/ErrorHist_SB_BinStrat2_10s.png",  
		hist2_out="Visualizations/ErrorHist_SB_BinStrat7_10s.png",
		hist1_title="Distribution of Error (10s scan, unoptimized)",  
		hist2_title="Distribution of Error (10s scan, optimized)",
		dataset="Datasets/results2.csv") 

def main_visualize():
	
	df = load_results("Datasets/results2.csv")
	days = [(2019, 1, 1), (2019, 4, 29)]
	
	"""
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=2, save_path="Visualizations/SB01_5s_2.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=6, save_path="Visualizations/SB01_5s_6.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=8, save_path="Visualizations/SB01_5s_8.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=2, save_path="Visualizations/SB02_5s_2.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=6, save_path="Visualizations/SB02_5s_6.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=8, save_path="Visualizations/SB02_5s_8.html", interval=5, results=(0, 100))
	"""
	
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=2, save_path="Visualizations/SB01_10s_2.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=7, save_path="Visualizations/SB01_10s_7.html", interval=10, results=(0, 100))
	#view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=9, save_path="Visualizations/SB01_10s_9.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=2, save_path="Visualizations/SB02_10s_2.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=7, save_path="Visualizations/SB02_10s_7.html", interval=10, results=(0, 100))
	#view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=9, save_path="Visualizations/SB02_10s_9.html", interval=10, results=(0, 100))

def main():
	main_optimize_bins()
	#main_test_alg()
	#main_compare_bins()
	#main_visualize()

if __name__ == "__main__":
	main()

	
	
	
