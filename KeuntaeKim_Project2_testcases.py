from KeuntaeKim_Project2 import read_input_file, gcd_list, heuristic_score, create_successors, a_star_search
import numpy as np
import unittest

class KeuntaeKimProject2Testcases(unittest.TestCase):
    def test_read_input_file(self):
        filename = "P1_Option2_WaterPitcher/cat test_input1.txt"  # Different from the original cat input*.txt
        pitchers, target_quantity = read_input_file(filename)
        self.assertTrue(len(pitchers) > 0)
        self.assertEqual(target_quantity, 7)
        print("test_read_input_file --- PASSED")

    def test_gcd_list(self):
        self.assertEqual(gcd_list([3, 6, 9]), 3)
        self.assertEqual(gcd_list([4, 8, 12]), 4)
        self.assertEqual(gcd_list([100, 300]), 100)
        print("test_gcd_list --- PASSED")

    def test_heuristic_score(self):
        state = (0, 0)
        pitchers = [3, 4, np.inf]
        target_quantity = 7
        self.assertTrue(heuristic_score(state, pitchers, target_quantity) >= 0)  # Heuristic score should be Positive!
        print("test_heuristic_score --- PASSED")

    def test_create_successors(self):
        state = (0, 0)
        pitchers = [3, 4, np.inf]
        successors = create_successors(state, pitchers)
        self.assertEqual(set(successors), {(3, 0), (0, 4), (0, 0)})
        print("test_create_successors --- PASSED")

    def test_a_star_search_1(self):
        pitchers = [3, 4, np.inf]
        target_quantity = 7
        steps = a_star_search(pitchers[:-1], target_quantity)  # Excluding the "infinite" pitcher for the A* Search.
        self.assertEqual(steps, 4)  # Example path: Fill 3, Fill 2, Fill into "infinite" pitcher from both(+2).
        print("test_a_star_search_1 --- PASSED")

    def test_a_star_search_2(self):
        pitchers = [3, 4, np.inf]
        target_quantity = 1
        steps = a_star_search(pitchers[:-1], target_quantity)
        self.assertEqual(steps, -1)  # '-1' means Unsolvable/No Path
        print("test_a_star_search_2 --- PASSED")


if __name__ == "__main__":
    unittest.main()
