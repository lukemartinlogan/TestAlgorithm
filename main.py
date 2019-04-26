
from TestData import *
from TestAlgorithm import *
from Visualize import *


def visualize():
	df = load_results("./results_SB_5s.csv")
	view_tests(df, building="SB", floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=4, save_path="./SB_01_R_NewBins2.html", results=(0, 1000))
	

def test_sim():
	
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
	

def test_alg():

	#Open the test cases for a certain building (5sec
	print("Opening test cases")
	cases = TestCases(out="results_SB_5s.csv")
	cases.open_test_data(path="database.csv", building="SB", interval=5)
	
	#Run the new bins over the new test data
	print("Testing bin strategy for 5 seconds")
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 4)
	cases.to_csv()
	
	#Run the new bins over the new test data
	print("Testing bin strategy for 10 seconds")
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 5)
	cases.to_csv()
	
	
	#Open the test cases for a certain building (5sec
	print("Opening test cases")
	cases = TestCases(out="results_SB_10s.csv")
	cases.open_test_data(path="database.csv", building="SB", interval=10)
	
	#Run the new bins over the new test data
	print("Testing new bin strategy for 5 seconds")
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 5)
	cases.to_csv()
	
	#Run the new bins over the new test data
	print("Testing new bin strategy for 10 seconds")
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 5)
	cases.to_csv()


def optimize_bins():

	#Open the test cases for a certain building
	print("Opening test cases")
	cases = TestCases()
	cases.open_test_data(building="SB", interval=10)
	
	#Run the new bins over the new test data
	print("Optimizing Bins")
	cases.optimize_bins(loc_alg=2, floor_alg=1, top_n=3, num_guesses = 100)

def main():
	test_alg()

if __name__ == "__main__":
	main()

	
	
	