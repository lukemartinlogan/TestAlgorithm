
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

def main_signal_stats():
	cases = TestCases()
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=5)
	ViewSignalStats(cases, hist_title="Signal Strengths in SB", hist_out="Visualizations/signal_strengths.png")
	
	
def main_optimize_bins():

	#Creating bin optimizer
	bins = BinOptimizer()
	
	#Open the test cases for a certain building (interval=5sec)
	print("Opening test cases - 5sec")
	bins.open_test_data(path="Datasets/database.csv", building="SB", interval=5)
	
	#Optimize
	print("Optimizing Bins")
	
	print(bins)

def main_test_alg():

	cases = TestCases(out="Datasets/results.csv")
	
	#Get the location estimates for the bin strategies (5s)
	print("Opening test cases -5sec")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=5)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 2, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 3, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 6, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 8, to_csv = True)
	
	#Get the location estimates for the bin strategies (10s)
	print("Opening test cases -10sec")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 2, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 3, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 7, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 9, to_csv = True)

def main_view_stats():
	df = pd.read_csv("Datasets/results.csv")
	
	print("Stats for 5s interval, strategy 2")
	ViewStats(bin_strat=2, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	
	#print("Stats for 5s interval, strategy 3")
	#ViewStats(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	
	print("Stats for 5s interval, strategy 6")
	ViewStats(bin_strat=6, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	
	print("Stats for 10s interval, strategy 2")
	ViewStats(bin_strat=2, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	
	#print("Stats for 10s interval, strategy 3")
	#ViewStats(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	
	print("Stats for 10s interval, strategy 7")
	ViewStats(bin_strat=7, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)

def main_compare_bins(): 
	CompareBinStrategies(
		bin_strat1=2, bin_strat2=6, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, 
		hist1_out="Visualizations/ErrorHist_SB_BinStrat2_5s.png",  
		hist2_out="Visualizations/ErrorHist_SB_BinStrat6_5s.png",
		hist1_title="Distribution of Error (5s scan, unoptimized)",  
		hist2_title="Distribution of Error (5s scan, optimized)",
		dataset="Datasets/results.csv")
	
	CompareBinStrategies(
		bin_strat1=2, bin_strat2=7, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, 
		hist1_out="Visualizations/ErrorHist_SB_BinStrat2_10s.png",  
		hist2_out="Visualizations/ErrorHist_SB_BinStrat7_10s.png",
		hist1_title="Distribution of Error (10s scan, unoptimized)",  
		hist2_title="Distribution of Error (10s scan, optimized)",
		dataset="Datasets/results.csv")

def main_visualize():
	
	df = load_results("Datasets/results.csv")
	days = [(2019, 1, 1), (2019, 4, 29)]
	
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=2, save_path="Visualizations/SB01_5s_2.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=6, save_path="Visualizations/SB01_5s_6.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=2, save_path="Visualizations/SB02_5s_2.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=6, save_path="Visualizations/SB02_5s_6.html", interval=5, results=(0, 100))
	
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=2, save_path="Visualizations/SB01_10s_2.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=7, save_path="Visualizations/SB01_10s_7.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=2, save_path="Visualizations/SB02_10s_2.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=7, save_path="Visualizations/SB02_10s_7.html", interval=10, results=(0, 100))
	
def main():
	main_signal_stats()
	#main_optimize_bins()
	#main_test_alg()
	#main_view_stats()
	#main_compare_bins()
	#main_visualize()

if __name__ == "__main__":
	main()

	
	
	
