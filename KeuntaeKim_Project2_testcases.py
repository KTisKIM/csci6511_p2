from KeuntaeKim_Project2 import *
import unittest

class KeuntaeKimProject2Testcases(unittest.TestCase):
    def init_setup(self):
        # Setup can include initializing landscapes, tiles, targets, etc., for testing purposes.
        self.landscape = [[0, 0, 1, 0], [0, 2, 0, 3], [3, 0, 0, 0], [0, 4, 0, 0]]
        self.tiles = {"FULL_BLOCK": 2, "OUTER_BOUNDARY": 2, "EL_SHAPE": 1}
        self.targets = {1: 1, 2: 1, 3: 1, 4: 1}
        self.position = (0, 0)
        print("init_setup --- COMPLETED")
    
    def test_is_valid(self):
        # Example test for is_valid
        self.assertTrue(is_valid(self.landscape, "FULL_BLOCK", self.position, self.targets, self.tiles))
        print("test_is_valid --- PASSED")
    
    def test_apply_tile(self):
        # Before application
        expected_before = 2
        self.assertEqual(self.tiles["FULL_BLOCK"], expected_before)
        print("test_apply_tile __ Before Application --- PASSED")
        
        # Apply tile
        apply_tile(self.landscape, "FULL_BLOCK", self.position, self.tiles)
        
        # After application
        expected_after = 1
        self.assertEqual(self.tiles["FULL_BLOCK"], expected_after)
        print("test_apply_tile __ After Application --- PASSED")
    
    def test_remove_tile(self):
        # Assume a tile is applied
        apply_tile(self.landscape, "FULL_BLOCK", self.position, self.tiles)
        remove_tile(self.landscape, "FULL_BLOCK", self.position, self.tiles)
        
        # Check if the tile count is restored
        expected_restore = 2
        self.assertEqual(self.tiles["FULL_BLOCK"], expected_restore)
        print("test_remove_tile --- PASSED")
    
    def test_ac3(self):
        # This would test the AC3 function's ability to reduce domains correctly
        # Setup a simple scenario where AC3 will modify the domains
        self.landscape = [[1, 2, 0, 0], [0, 0, 3, 4], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.tiles = {"FULL_BLOCK": 1, "OUTER_BOUNDARY": 1, "EL_SHAPE": 1}
        self.targets = {1: 1, 2: 1, 3: 1, 4: 1}

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

        # Simulate arcs for this scenario
        arcs = initialize_arcs(variables)

        csp = {
            "landscape": self.landscape,
            "tiles": self.tiles,
            "targets": self.targets,
            "variables": variables,
            "arcs": arcs,
            "domains": domains
        }

        # Apply AC3 algorithm
        result = ac3(csp)

        # Check if AC3 successfully reduced the domains
        self.assertTrue(result)  # AC3 should return True indicating possible consistency
        for domain in csp["domains"].values():
            # Assuming that domains should be reduced based on the constraints applied
            self.assertLess(len(domain), len(tile_patterns.keys()))  # Domains should be reduced in size


if __name__ == "__main__":
    unittest.main()
