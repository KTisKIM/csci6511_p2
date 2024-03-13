from KeuntaeKim_Project2 import *
import unittest

class KeuntaeKimProject2Testcases(unittest.TestCase):
    def test_read_input_file(self):
        filename = "Option 3_Tile Placement/tileplacement/tilesproblem_unittest.txt"
        landscape, tiles, targets, _ = read_input_file(filename)
        
        self.assertTrue(len(landscape) > 0)
        self.assertEqual(tiles, {"EL_SHAPE": 7, "OUTER_BOUNDARY": 7, "FULL_BLOCK": 11})
        self.assertEqual(targets, {1: 11, 2: 26, 3: 21, 4: 20})
        print("test_read_input_file --- PASSED")

    def test_is_valid(self):
        landscape = [[0, 0, 1, 0], [0, 2, 0, 3], [3, 0, 0, 0], [0, 4, 0, 0]]
        tiles = {"FULL_BLOCK": 2, "OUTER_BOUNDARY": 2, "EL_SHAPE_0": 1}
        targets = {1: 1, 2: 1, 3: 1, 4: 1}
        position = (0, 0)
        
        self.assertTrue(is_valid(landscape, "FULL_BLOCK", position, targets, tiles))
        print("test_is_valid --- PASSED")
    
    def test_apply_tile(self):
        landscape = [[0, 0, 1, 0], [0, 2, 0, 3], [3, 0, 0, 0], [0, 4, 0, 0]]
        tiles = {"FULL_BLOCK": 2, "OUTER_BOUNDARY": 2, "EL_SHAPE_0": 1}
        targets = {1: 1, 2: 1, 3: 1, 4: 1}
        position = (0, 0)
        
        # Before application
        self.assertEqual(tiles["FULL_BLOCK"], 2)
        print("test_apply_tile __ Before Application --- PASSED")
        
        # Apply tile
        apply_tile(landscape, "FULL_BLOCK", position, tiles)
        
        # After application
        self.assertEqual(tiles["FULL_BLOCK"], 1)
        print("test_apply_tile __ After Application --- PASSED")
    
    def test_remove_tile(self):
        landscape = [[0, 0, 1, 0], [0, 2, 0, 3], [3, 0, 0, 0], [0, 4, 0, 0]]
        tiles = {"FULL_BLOCK": 2, "OUTER_BOUNDARY": 2, "EL_SHAPE_0": 1}
        targets = {1: 1, 2: 1, 3: 1, 4: 1}
        position = (0, 0)
        
        # Assume a tile is applied
        apply_tile(landscape, "FULL_BLOCK", position, tiles)
        remove_tile(landscape, "FULL_BLOCK", position, tiles)
        
        # Check if the tile count is restored
        self.assertEqual(self.tiles["FULL_BLOCK"], 2)
        print("test_remove_tile --- PASSED")
    
    def test_ac3(self):
        # Test the AC3 function to reduce domains correctly
        # Setup a simple test where AC3 will modify the domains
        landscape = [[1, 2, 0, 0], [0, 0, 3, 4], [0, 0, 0, 0], [0, 0, 0, 0]]
        tiles = {"FULL_BLOCK": 1, "OUTER_BOUNDARY": 1, "EL_SHAPE": 1}
        targets = {1: 1, 2: 1, 3: 1, 4: 1}

        # Define variables based on the simplified landscape
        variables = [(0, 0), (0, 2)]
        
        # Simplified tile patterns for the purpose of testing
        tile_patterns = {
            "FULL_BLOCK": [(0, 0), (0, 1), (1, 0), (1, 1)],
            "OUTER_BOUNDARY": [(0, 0), (0, 1), (1, 0), (2, 0), (0, 2), (1, 2), (2, 2), (2, 1)],
            "EL_SHAPE": [(0, 0), (0, 1), (0, 2), (1, 0)]
        }

        # Initialize domains for each variable (position)
        domains = {variable: list(tile_patterns.keys()) for variable in variables}

        # Simulate arcs for the scenario
        arcs = initialize_arcs(variables)

        csp = {
            "landscape": landscape,
            "tiles": tiles,
            "targets": targets,
            "variables": variables,
            "arcs": arcs,
            "domains": domains
        }

        # Apply AC3 algorithm
        result = ac3(csp)

        # Check if AC3 successfully reduced the domains
        self.assertTrue(result)  # AC3 should return True indicating possible consistency
        print("test_ac3 __ After AC3 --- PASSED")
        for domain in csp["domains"].values():
            # Assuming that domains should be reduced based on the constraints applied
            self.assertLess(len(domain), len(tile_patterns.keys()))  # Domains should be reduced in size
        print("test_ac3 __ Reduced domains --- PASSED")


if __name__ == "__main__":
    unittest.main()
