from KeuntaeKim_Project2 import *
import unittest

class KeuntaeKimProject2Testcases(unittest.TestCase):
    def test_read_input_file(self):
        filename = "Option 3_Tile Placement/tileplacement/tilesproblem_unittest.txt"
        landscape, tiles, targets, _ = read_input_file(filename)
        
        self.assertTrue(len(landscape) > 0)
        self.assertEqual(tiles, {"EL_SHAPE": 7, "OUTER_BOUNDARY": 7, "FULL_BLOCK": 11})
        self.assertEqual(targets, {1: 11, 2: 26, 3: 21, 4: 20})
        print("\n>>>>> test_read_input_file --- PASSED")

    def test_apply_and_remove_tile(self):
        filename = "Option 3_Tile Placement/tileplacement/tilesproblem_unittest.txt"
        landscape, tiles, targets, _ = read_input_file(filename)
        
        # landscape = [[0, 0, 1, 0], [0, 2, 0, 3], [3, 0, 0, 0], [0, 4, 0, 0]]
        # tiles = {"FULL_BLOCK": 2, "OUTER_BOUNDARY": 2, "EL_SHAPE": 1}
        # targets = {1: 0, 2: 0, 3: 0, 4: 0}
        # position = (0, 0)
        
        tile_size = 4
        landscape_size = len(landscape)  # Assume landscape is a list of lists representing the grid
        variables = [(i, j) for i in range(0, landscape_size, tile_size)
                    for j in range(0, landscape_size, tile_size)]
        # Initialize domains for each variable (position)
        # Assume "tiles" contains the types of tiles as keys
        tile_types = list(tiles.keys())  # This list should contain your tile types, ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']
        domains = {variable: tile_types for variable in variables}
        csp = {
            "landscape": landscape,
            "tiles": tiles,
            "targets": targets,
            "variables": variables,
            "arcs": initialize_arcs(variables),
            "domains": domains
        }
        original_numbers = {}
        assignment = {}
        position = select_unassigned_tile_spot(csp, assignment, original_numbers)  # position
        # print("이거 뭐지", position)  # TODO
        
        original_landscape = [row[:] for row in landscape]
        
        # print("before apply tile", [print(row) for row in landscape])  # TODO
        # See if the apply_tile() and remove_tile() work correctly
        apply_tile(landscape, "FULL_BLOCK", position, tiles, original_numbers)
        # print("after apply tile", [print(row) for row in landscape])  # TODO
        remove_tile(landscape, "FULL_BLOCK", position, tiles, original_numbers)
        # print("after remove tile", [print(row) for row in landscape])  # TODO
        
        self.assertEqual(landscape, original_landscape)  # Check if the Landscape is reverted back to the original after the remove_tile()
        print("\n>>>>> test_apply_and_remove_tile --- PASSED")
        
    def test_is_valid(self):
        filename = "Option 3_Tile Placement/tileplacement/tilesproblem_unittest.txt"
        landscape, tiles, targets, _ = read_input_file(filename)
        
        # # Check if placing a FULL_BLOCK tile at (0, 0) position is possible.
        # landscape = [[0, 0, 1, 0], [0, 2, 0, 3], [3, 0, 0, 0], [0, 4, 0, 0]]
        # tiles = {"FULL_BLOCK": 2, "OUTER_BOUNDARY": 2, "EL_SHAPE": 1}
        # targets = {1: 0, 2: 0, 3: 0, 4: 0}
        # position = (0, 0)
        
        tile_size = 4
        landscape_size = len(landscape)  # Assume landscape is a list of lists representing the grid
        variables = [(i, j) for i in range(0, landscape_size, tile_size)
                    for j in range(0, landscape_size, tile_size)]
        # Initialize domains for each variable (position)
        # Assume "tiles" contains the types of tiles as keys
        tile_types = list(tiles.keys())  # This list should contain your tile types, ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']
        domains = {variable: tile_types for variable in variables}
        csp = {
            "landscape": landscape,
            "tiles": tiles,
            "targets": targets,
            "variables": variables,
            "arcs": initialize_arcs(variables),
            "domains": domains
        }
        original_numbers = {}
        assignment = {}
        position = select_unassigned_tile_spot(csp, assignment, original_numbers)  # position
        
        self.assertTrue(is_valid(landscape, "FULL_BLOCK", position, tiles))
        print("\n>>>>> test_is_valid --- PASSED")

    def test_ac3(self):
        filename = "Option 3_Tile Placement/tileplacement/tilesproblem_unittest.txt"
        landscape, tiles, targets, _ = read_input_file(filename)
        
        # landscape = [[0, 0, 1, 0], [0, 2, 0, 3], [3, 0, 0, 0], [0, 4, 0, 0]]
        # tiles = {"FULL_BLOCK": 2, "OUTER_BOUNDARY": 2, "EL_SHAPE": 1}
        # targets = {1: 0, 2: 0, 3: 0, 4: 0}
        
        tile_size = 4
        landscape_size = len(landscape)  # Assume landscape is a list of lists representing the grid
        variables = [(i, j) for i in range(0, landscape_size, tile_size)
                    for j in range(0, landscape_size, tile_size)]
        # Initialize domains for each variable (position)
        # Assume "tiles" contains the types of tiles as keys
        tile_types = list(tiles.keys())  # This list should contain your tile types, ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']
        domains = {variable: tile_types for variable in variables}
        csp = {
            "landscape": landscape,
            "tiles": tiles,
            "targets": targets,
            "variables": variables,
            "arcs": initialize_arcs(variables),
            "domains": domains
        }
        
        # Test and Check if AC3 algorithm reduces CSP's domains.
        self.assertTrue(ac3(csp))
        print("\n>>>>> test_ac3 --- PASSED")

    def test_backtrack(self):
        filename = "Option 3_Tile Placement/tileplacement/tilesproblem_unittest.txt"
        landscape, tiles, targets, _ = read_input_file(filename)
        
        # landscape = [[0, 0, 1, 0], [0, 2, 0, 3], [3, 0, 0, 0], [0, 4, 0, 0]]
        # tiles = {"FULL_BLOCK": 2, "OUTER_BOUNDARY": 2, "EL_SHAPE": 1}
        # targets = {1: 0, 2: 0, 3: 0, 4: 0}
        
        tile_size = 4
        landscape_size = len(landscape)  # Assume landscape is a list of lists representing the grid
        variables = [(i, j) for i in range(0, landscape_size, tile_size)
                    for j in range(0, landscape_size, tile_size)]
        # Initialize domains for each variable (position)
        # Assume "tiles" contains the types of tiles as keys
        tile_types = list(tiles.keys())  # This list should contain your tile types, ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']
        domains = {variable: tile_types for variable in variables}
        csp = {
            "landscape": landscape,
            "tiles": tiles,
            "targets": targets,
            "variables": variables,
            "arcs": initialize_arcs(variables),
            "domains": domains
        }
        original_numbers = {}
        assignment = {}
        
        # Check if the backtracking function finds valid solutions
        self.assertIsNotNone(backtrack(assignment, csp, original_numbers))
        print("\n>>>>> test_backtrack --- PASSED")


if __name__ == "__main__":
    unittest.main()
