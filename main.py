
"""
This file contains a loose collection of test cases I ran during the semester.
"""

from TestData import *
from TestAlgorithm import *
from Visualize import *
from OptimizeBins import *
from AnalyzeAlgorithm import *
from AnalyzeSignals import *
import pandas as pd

def main_download_database():
	#download_test_data1(out="Datasets/full_database.csv")
	download_beacons(out="Datasets/beacons.csv")
	download_gateways(loc="Datasets/gateways.json",out="Datasets/gateways.csv")

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

	"""
	#Open test data for 10sec interval
	print("Opening test cases - 10sec")
	cases = TestCases()
	cases.open_test_data(database="Datasets/database.csv", building="SB", interval=10, days=[(2019, 1, 1), (2019, 4, 28)])

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
	"""

def main_test_alg():

	cases = TestCases(out="Datasets/results.csv")

	#Get the location estimates for the bin strategies (5s)
	print("Opening test cases -5sec")
	cases.open_test_data(database="Datasets/database.csv", building="SB", interval=5)
	cases.test_algorithm(loc_alg = 2, floor_alg = 2, bin_strategy = 3, top_n=3, to_csv = True, reset_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 2, bin_strategy = 10, top_n=3, to_csv = True)

	#Get the location estimates for the bin strategies (10s)
	print("Opening test cases -10sec")
	cases.open_test_data(database="Datasets/database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = 2, floor_alg = 2, bin_strategy = 3, top_n=3, to_csv = True)
	cases.test_algorithm(loc_alg = 2, floor_alg = 2, bin_strategy = 11, top_n=3, to_csv = True)

def main_view_stats():
	df = pd.read_csv("Datasets/results.csv")

	"""
	print("Stats for 5s interval, strategy 3")
	ViewStats(
		bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df,
		hist_title="",
		hist_out="Visualizations/SB_err_hist_strat3_5s.png")
	"""

	print("Stats for 5s interval, strategy 10")
	ViewStats(
		bin_strat=10, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df,
		hist_title="",
		hist_out="Visualizations/SB_err_hist_strat10_5s.png")

	"""
	print("Stats for 10s interval, strategy 3")
	ViewStats(
		bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df,
		hist_title="",
		hist_out="Visualizations/SB_err_hist_strat3_10s.png")
	"""

	print("Stats for 10s interval, strategy 11")
	ViewStats(
		bin_strat=11, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df,
		hist_title="",
		hist_out="Visualizations/SB_err_hist_strat11_10s.png")

def main_error_hist_mat():
	df = pd.read_csv("Datasets/results.csv")

	plt.figure(figsize=(7,2.25))

	print("Stats for 5s interval, strategy 3")
	error = GetErrors(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	plt.subplot(121)
	plt.hist(error, facecolor='blue', range=(0, 14), bins=10)
	plt.yticks(range(0, 20, 4))
	plt.title("5s, Initial")

	print("Stats for 5s interval, strategy 10")
	error = GetErrors(bin_strat=10, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	plt.subplot(122)
	plt.hist(error, facecolor='blue', range=(0, 14), bins=10)
	plt.yticks(range(0, 20, 4))
	plt.title("5s, Optimized")

	plt.savefig("Visualizations/error_hist_row_5s.png", bbox_inches='tight')
	plt.close()

	plt.figure(figsize=(7,2.25))

	print("Stats for 10s interval, strategy 3")
	error = GetErrors(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	plt.subplot(121)
	plt.hist(error, facecolor='blue', range=(0, 14), bins=10)
	plt.yticks(range(0, 20, 4))
	plt.title("10s, Initial")

	print("Stats for 10s interval, strategy 11")
	error = GetErrors(bin_strat=11, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	plt.subplot(122)
	plt.hist(error, facecolor='blue', range=(0, 14), bins=10)
	plt.yticks(range(0, 20, 4))
	plt.title("10s, Optimized")

	plt.savefig("Visualizations/error_hist_row_10s.png", bbox_inches='tight')
	plt.close()

def main_visualize():

	results = pd.read_csv("Datasets/results.csv")
	database = pd.read_csv("Datasets/database.csv")

	days = [(2019, 1, 1), (2019, 4, 28)]

	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=3, save_path="Visualizations/SB01_5s_3.html", interval=5, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=10, save_path="Visualizations/SB01_5s_10.html", interval=5, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=3, save_path="Visualizations/SB02_5s_3.html", interval=5, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=10, save_path="Visualizations/SB02_5s_10.html", interval=5, num_results=100)

	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=3, save_path="Visualizations/SB01_10s_3.html", interval=10, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=11, save_path="Visualizations/SB01_10s_11.html", interval=10, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=3, save_path="Visualizations/SB02_10s_3.html", interval=10, num_results=100)
	view_tests(results=results, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=11, save_path="Visualizations/SB02_10s_11.html", interval=10, num_results=100)

def main_visualize_beacons():

	database = pd.read_csv("Datasets/full_database.csv")

	days = [(2019, 1, 1), (2019, 3, 29)]

	view_tests(results=None, database=database, building="SB", loc_alg=2, floor=1, days=days, bin_strategy=3, save_path="Visualizations/SB01_beacons.html", interval=5, num_results=100)
	view_tests(results=None, database=database, building="SB", loc_alg=2, floor=2, days=days, bin_strategy=3, save_path="Visualizations/SB02_beacons.html", interval=5, num_results=100)

def main_visualize_testpos():

	database = pd.read_csv("Datasets/full_database.csv")

	#SBO1 Test Positions
	cases = TestCases()
	cases.open_test_cases(
		cases=[
			"Test57096", "Test57613", "Test71012", "Test81299", "Test44031",
			"Test63717", "Test99541", "Test13099", "Test94635", "Test88339",
			"Test50868", "Test5987"
		],
		database="Datasets/database.csv",
		results="Datasets/results.csv",
		bin_strategy=3
	)
	view_test_positions(cases, building="SB", floor=1, top_n=3, portrait=False, save_path="Visualizations/SB01_positions.html")
	
	cases.open_test_cases(
		cases=[
			"Test57096", "Test57613", "Test71012", "Test81299", "Test44031",
			"Test63717", "Test99541", "Test13099", "Test94635", "Test88339",
			"Test50868", "Test5987"
		],
		database="Datasets/database.csv",
		results="Datasets/results.csv",
		bin_strategy=11
	)
	view_test_positions(cases, building="SB", floor=1, top_n=3, portrait=False, save_path="Visualizations/SB01_est-optimized.html")

def main_visualize_tests():

	database = pd.read_csv("Datasets/full_database.csv")

	#SBO1 Test Positions
	cases = TestCases()
	cases.open_test_cases(
		cases=[
			"Test57096", "Test57613", "Test71012", "Test81299", "Test44031",
			"Test63717", "Test99541", "Test13099", "Test23777", "Test88339",
			"Test50868", "Test5987"
		],
		database="Datasets/database.csv",
		results="Datasets/results.csv",
		bin_strategy=3
	)
	view_test_cases(cases, building="SB", floor=1, top_n=3, portrait=False, save_path="Visualizations/SB01_est-unoptimized.html")

	cases.open_test_cases(
		cases=[
			"Test57096", "Test57613", "Test71012", "Test81299", "Test44031",
			"Test63717", "Test99541", "Test13099", "Test23777", "Test88339",
			"Test50868", "Test5987"
		],
		database="Datasets/database.csv",
		results="Datasets/results.csv",
		bin_strategy=11
	)
	view_test_cases(cases, building="SB", floor=1, top_n=3, portrait=False, save_path="Visualizations/SB01_est-optimized.html")

def main_find_outliers():

	results = pd.read_csv("Datasets/results.csv")
	database = pd.read_csv("Datasets/database.csv")

	days=[(2019, 1, 1), (2019, 4, 29)]

	view_tests(
		results=results, database=database, building="SB", loc_alg=2, floor=1,
		days=days,
		bin_strategy=10, save_path="Visualizations/SB01_5s_3_outliers.html",
		interval=5,
		xy_error=11,
		num_results=100)

	view_tests(
		results=results, database=database, building="SB", loc_alg=2, floor=1,
		days=days,
		bin_strategy=3, save_path="Visualizations/SB01_10s_11_outliers.html",
		interval=10,
		xy_error=11,
		num_results=100)

def main_visualize_outlier():
	cases = TestCases()
	"""
	cases.open_test_cases(
		#cases=["Test50868"], database="Datasets/database.csv", results="Datasets/results.csv",
		#cases=["Test86285"], database="Datasets/database.csv", results="Datasets/results.csv",
		cases=["Test23777"], database="Datasets/database.csv", results="Datasets/results.csv",
		loc_alg=2, floor_alg=1, bin_strategy=3, top_n=3
	)
	"""

	"""
	cases.open_test_cases(
		cases=["Test83075"], database="Datasets/database.csv", results="Datasets/results.csv",
		loc_alg=2, floor_alg=1, bin_strategy=10, top_n=3
	)
	"""

	cases.open_test_cases(
		cases=["Test24720"], database="Datasets/database.csv", results="Datasets/results.csv",
		loc_alg=2, floor_alg=2, bin_strategy=10, top_n=3
	)

	view_test_cases(cases,  building="SB", floor=2, top_n=3, portrait=False, save_path="Visualizations/Test24720.html")
	for case in cases.test_cases.values():
		for b in case.beacons:
			print(str(b))
	return

def main_get_cdfs():
	df = pd.read_csv("Datasets/results.csv")

	##########
	plt.figure(figsize=(7,2.25))
	error = GetErrors(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	n, bins, patches = plt.hist(
		error, facecolor='blue', range=(0, 14), bins=500,
		histtype='step', density=True, cumulative=True,
		label="Initial")
	error = GetErrors(bin_strat=10, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	n, bins, patches = plt.hist(
		error, facecolor='blue', range=(0, 14), bins=500,
		histtype='step', density=True, cumulative=True,
		label="Optimized")
	plt.legend(loc="lower center")
	plt.xlabel("X (meters)")
	plt.ylabel("Probability")
	plt.title("P(error <= X meters) For 5s Tests")
	plt.savefig("Visualizations/error_cdf_row_5s.png", bbox_inches='tight')
	plt.close()

	#############
	plt.figure(figsize=(7,2.25))
	error = GetErrors(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	n, bins, patches = plt.hist(
		error, facecolor='blue', range=(0, 14), bins=500,
		histtype='step', density=True, cumulative=True,
		label="Initial")
	error = GetErrors(bin_strat=11, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	n, bins, patches = plt.hist(
		error, facecolor='blue', range=(0, 14),
		bins=500, histtype='step', density=True, cumulative=True,
		label="Optimized")
	plt.legend(loc="lower center")
	plt.xlabel("X (meters)")
	plt.ylabel("Probability")
	plt.title("P(error <= X meters) For 10s Tests")
	plt.savefig("Visualizations/error_cdf_row_10s.png", bbox_inches='tight')
	plt.close()

def main_floor_error():

	df = pd.read_csv("Datasets/results.csv")
	print(df[["testid", "floor_true", "floor_est", "interval", "bin_strat"]][df["floor_error"] != 0])

def main_error_le_x():
	df = pd.read_csv("Datasets/results.csv")
	x = 14

	#Unoptimized, 5s
	error = GetErrors(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	error2 = error[error <= x]
	print("Unoptimized, 5s: " + str(len(error2)/len(error)))

	#Unoptimized, 10s
	error = GetErrors(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	error2 = error[error <= x]
	print("Unoptimized, 10s: " + str(len(error2)/len(error)))

	#Optimized, 5s
	error = GetErrors(bin_strat=10, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	error2 = error[error <= x]
	print("Optimized, 5s: " + str(len(error2)/len(error)))

	#Optimized, 10s
	error = GetErrors(bin_strat=11, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	error2 = error[error <= x]
	print("Optimized, 10s: " + str(len(error2)/len(error)))

def main_median_error():
	df = pd.read_csv("Datasets/results.csv")

	#Unoptimized, 5s
	error = GetErrors(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	print("Unoptimized, 5s: " + str(error.median()))

	#Unoptimized, 10s
	error = GetErrors(bin_strat=3, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	print("Unoptimized, 10s: " + str(error.median()))

	#Optimized, 5s
	error = GetErrors(bin_strat=10, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=5, df=df)
	print("Optimized, 5s: " + str(error.median()))

	#Optimized, 10s
	error = GetErrors(bin_strat=11, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, df=df)
	print("Optimized, 10s: " + str(error.median()))


def main():
	#main_download_database()
	#main_signal_stats()
	#main_optimize_bins()
	#main_test_alg()
	#main_view_stats()
	#main_error_hist_mat()
	#main_visualize()
	#main_visualize_beacons()
	#main_visualize_testpos()
	main_visualize_tests()
	#main_find_outliers()
	#main_visualize_outlier()
	#main_get_cdfs()
	#main_error_le_x()
	#main_median_error()
	#main_floor_error()

if __name__ == "__main__":
	main()
