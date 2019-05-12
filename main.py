
from TestData import *
from TestAlgorithm import *
from Visualize import *
from OptimizeBins import *

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
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 3)
	cases.to_csv()


def main_optimize_bins():

	#Creating bin optimizer
	bins = BinOptimizer()

	#Open the test cases for a certain building (interval=10sec)
	print("Opening test cases - 10sec")
	bins.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	
	#Genetic optimization
	print("Optimizing Bins")
	bins.optimize(loc_alg=loc_algorithms[2], floor_alg=floor_algorithms[1], top_n=3, pop_size = 20, num_generations=100)
	print(bins)

	#Open the test cases for a certain building (interval = 5sec)
	print("Opening test cases - 5sec")
	bins.open_test_data(path="Datasets/database.csv", building="SB", interval=5)
	
	#Genetic optimization
	print("Optimizing Bins")
	bins.optimize(loc_alg=loc_algorithms[2], floor_alg=floor_algorithms[1], top_n=3, pop_size = 20, num_generations=100)
	print(bins)
	

def main_visualize():
	
	df = load_results("Datasets//results_SB_5s.csv")
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=2, save_path="Visualizations/SB01_5s_2.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=4, save_path="Visualizations/SB01_5s_4.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=6, save_path="Visualizations/SB01_5s_6.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=2, save_path="Visualizations/SB02_5s_2.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=4, save_path="Visualizations/SB02_5s_4.html", interval=5, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=6, save_path="Visualizations/SB02_5s_6.html", interval=5, results=(0, 100))
		
	df = load_results("Datasets//results_SB_10s.csv")
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=2, save_path="Visualizations/SB01_10s_2.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=5, save_path="Visualizations/SB01_10s_5.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=7, save_path="Visualizations/SB01_10s_7.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=2, save_path="Visualizations/SB02_10s_2.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=5, save_path="Visualizations/SB02_10s_5.html", interval=10, results=(0, 100))
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=7, save_path="Visualizations/SB02_10s_7.html", interval=10, results=(0, 100))
	

def main_test_alg2_interval_bins():

	#Open the test cases for a certain building (5sec)
	print("Opening test cases - 5sec")
	cases = TestCases(out="Datasets/results_SB_5s.csv")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=5)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[2], to_csv = True)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[4], to_csv = True)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[6], to_csv = True)
	
	
	#Open the test cases for a certain building (5sec)
	print("Opening test cases - 10sec")
	cases = TestCases(out="Datasets/results_SB_10s.csv")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[2], to_csv = True)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[5], to_csv = True)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[7], to_csv = True)


def main_test_alg123():

	#Open the test cases for a certain building (5sec)
	print("Opening test cases - 10sec")
	cases = TestCases(out="Datasets/results_SB_5s.csv")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = loc_algorithms[1], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[7])
	print(cases.net_xy_error)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[7])
	print(cases.net_xy_error)
	cases.test_algorithm(loc_alg = loc_algorithms[3], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[7])
	print(cases.net_xy_error)


def main_optimize_algorithm_bins():

	#Creating bin optimizer
	bins = BinOptimizer()
	
	print("Opening test cases - 10sec")
	bins.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	
	print("Optimizing Bins - Alg 1")
	bins.optimize(loc_alg=loc_algorithms[1], floor_alg=floor_algorithms[1], top_n=3, pop_size = 50, num_generations=100)
	print(bins)
	
	print("Optimizing Bins - Alg 3")
	bins.optimize(loc_alg=loc_algorithms[3], floor_alg=floor_algorithms[1], top_n=3, pop_size = 50, num_generations=100)
	print(bins)


def main_compare_algorithms():

	#Open the test cases for a certain building (5sec)
	print("Opening test cases - 10sec")
	cases = TestCases(out="Datasets/results_diff_algs.csv")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = loc_algorithms[1], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[8], to_csv = True)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[9], to_csv = True)
	cases.test_algorithm(loc_alg = loc_algorithms[3], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[10], to_csv = True)

def main():
	#main_optimize_bins()
	#main_test_alg2_interval_bins()
	#main_visualize()
	#main_optimize_algorithm_bins()
	#main_test_alg123()
	main_compare_algorithms()

if __name__ == "__main__":
	main()

	
	
	