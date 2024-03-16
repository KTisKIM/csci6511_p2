#################################################################
###                                                           ###
###     Name:      Keuntae Kim                                ###
###     GWID:      G30341718                                  ###
###     Course:    CSCI 6511(AI) - Online                     ###
###     Project:   2-Constraint Satisfaction Problems (CSP)   ###
###     Option:    3. Tile Placement                          ###
###                                                           ###
#################################################################

from collections import deque
import copy


def read_input_file(filename):
    """
    Reads Landscape, Tiles, Targets, and Solution Key(if needed in case) from the input file.
    """
    # Initialize variables
    landscape = []
    tiles = {}
    targets = {}
    solution_key = []
    
    # Identify where it's reading the input file
    read_landscape = False
    read_tiles = False
    read_targets = False
    read_solution_key = False
    
    # Read input file
    with open(filename, "r") as file:
        lines = file.readlines()
    
        for line in lines:
            list_current_line = []  # Store current line's items into a list
            # line = line.strip()  # <-- If I use strip(), then it will remove the very first empty space. Can't use it
            line = line.strip("")[:-1]  # This will not get rid of the FIRST empty space, and get rid of last empty space
            if line.startswith("# Landscape"):  ### Landscape Title line
                read_landscape = True
            elif line.startswith("# Tiles:"):   ### Tiles Title line
                if read_solution_key != True:
                    read_landscape = False
                    read_tiles = True
                elif read_solution_key == True:  # To filter out the solution key's tiles
                    # print("This is the Solution Key's Tiles.")
                    None
                else:
                    print("ERROR: It's reading something wrong!")
            elif line.startswith("# Targets:"):  ### Targets Title line
                read_tiles = False
                read_targets = True
            elif line.startswith("# Tiles Problem Solution Key"):  ### Solution Key Title line (if needed for testing in case)
                read_targets = False
                read_solution_key = True
                
            elif line and read_landscape:   ##### Landscape
                was_previous_empty = False  # Initialize: Check if previous item was empty
                for number in line.split(" "):
                    if number.isdigit():    # When it's a number
                        list_current_line.append(int(number))
                        was_previous_empty = False
                    else:  # when it's an empty space
                        if not was_previous_empty:  # If previous was not empty space, this is the first empty
                            was_previous_empty = True
                        elif number == "":
                            list_current_line.append(0)  # "0" here shows the empty spaces
                            was_previous_empty = False   # Reset the status after taking care of consecutive empty space
                landscape.append(list_current_line)      # Add the whole list(single line) to the landscape
            elif line and read_tiles:  ##### Tiles
                tiles_list = line.strip("{}").split(", ")
                for tile in tiles_list:
                    tile_shape, tile_counts = tile.split("=")
                    tiles[tile_shape] = int(tile_counts)
            elif line and read_targets:  ##### Targets
                bush, bush_counts = line.split(":")
                targets[int(bush)] = int(bush_counts)
            elif line and read_solution_key:  ##### Solution Key (if needed for testing in case)
                tile_solution = line.split()
                index = int(tile_solution[0])
                tile_size = int(tile_solution[1])
                tile_shape = tile_solution[2]
                solution_key.append([index, tile_size, tile_shape])
            else:  ### No-needed lines. Doesn't do anything
                # print("<< non defined >>")
                None
    
    ### To see if the function parsed the input file correctly
    # print("Landscape:\n", [print(row) for row in landscape])  # print statement appears above the "Landscape:" for some reason
    # print("Tiles:\n", tiles)
    # print("Targets:\n", targets)
    # print("Solution Key:\n", [print(index) for index in solution_key])  # print statement appears above the "Solution Key:" for some reason

    return landscape, tiles, targets, solution_key

def apply_tile(landscape, tile_shape, position, tiles, original_numbers):
    """
    Place the tile on the landscape and update visibility accordingly(to show it's covered by the tile).
    """
    # x, y = position --> x, y basically denote the top-left corner where the tile will be placed

    # Define the patterns for each tile_shape in terms of offsets from the top-left corner
    tile_patterns = {
        "FULL_BLOCK": [(d_x, d_y) for d_x in range(4) for d_y in range(4)],
        "OUTER_BOUNDARY": [(d_x, d_y) for d_x in range(4) for d_y in range(4) if d_x in [0, 3] or d_y in [0, 3]],
        "EL_SHAPE_0": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)],   # No rotate, original shape
        "EL_SHAPE_90": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)],  # Rotated 90 degree
        "EL_SHAPE_180": [(3, 0), (3, 1), (3, 2), (3, 3), (0, 3), (1, 3), (2, 3)], # Rotated 180 degree
        "EL_SHAPE_270": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]  # Rotated 270 degree
    }
    
    # Get the tile pattern for the given tile_shape
    pattern = tile_patterns[tile_shape]
    max_row = len(landscape)
    max_col = len(landscape[0]) if max_row > 0 else 0
    
    # Apply the tile by setting the covered positions to a specific non-zero value
    for d_x, d_y in pattern:
        x, y = position[0] + d_x, position[1] + d_y
        # Check if the position is within the bounds of the landscape
        if 0 <= x < max_row and 0 <= y < max_col:
            original_numbers[(x, y)] = landscape[x][y]  # Store the original numbers that were in the positions
            landscape[x][y] = 9                         # "9" indicates the presence of a tile/part of a tile

    # Reduce the quantity of the corresponding tile shape in tiles
    base_tile_shape = tile_shape.split("_")[0] + "_" + tile_shape.split("_")[1]  # EL_SHAPE_90 -> EL_SHAPE
    tiles[base_tile_shape] -= 1

def remove_tile(landscape, tile_shape, position, tiles, original_numbers):
    """
    Remove the tile from the landscape, reverting visibility changes(=back to the original).
    Basically, reverse the operation done by apply_tile(). Double make sure the landscape is
    reverted to its state before the tile was placed.
    """
    # Define the patterns for each tile shape in terms of offsets from the top-left corner
    tile_patterns = {
        "FULL_BLOCK": [(d_x, d_y) for d_x in range(4) for d_y in range(4)],
        "OUTER_BOUNDARY": [(d_x, d_y) for d_x in range(4) for d_y in range(4) if d_x in [0, 3] or d_y in [0, 3]],
        "EL_SHAPE_0": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)],   # No rotate, original shape
        "EL_SHAPE_90": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)],  # Rotated 90 degree
        "EL_SHAPE_180": [(3, 0), (3, 1), (3, 2), (3, 3), (0, 3), (1, 3), (2, 3)], # Rotated 180 degree
        "EL_SHAPE_270": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]  # Rotated 270 degree
    }
    
    # Get the tile pattern for the given "tile_shape"
    pattern = tile_patterns[tile_shape]
    
    # Remove the tile by setting the covered positions back to what it was
    for d_x, d_y in pattern:
        x, y = position[0] + d_x, position[1] + d_y
        if (x, y) in original_numbers:
            landscape[x][y] = original_numbers[(x, y)]  # Revert it back to the original number
            del original_numbers[(x, y)]                # Delete the restored number from the orignal_numbers
        
    # Increase back the quantity of the corresponding tile shape in tiles
    base_tile_shape = tile_shape.split("_")[0] + "_" + tile_shape.split("_")[1]  # EL_SHAPE_90 -> EL_SHAPE
    tiles[base_tile_shape] += 1

    return landscape

def is_valid(landscape, tile_shape, position, tiles):
    """
    Check if placing a tile at the position is valid(overlaps with any other existing tile?) according
    to the landscape and all the constraints. This considers the tile's shape, boundary, and the number
    of tiles left after placing the tile and see if it still meets the target requirements.
    """
    # Define the patterns for each tile shape in terms of offsets from the top-left corner
    tile_patterns = {
        "FULL_BLOCK": [(d_x, d_y) for d_x in range(4) for d_y in range(4)],
        "OUTER_BOUNDARY": [(d_x, d_y) for d_x in range(4) for d_y in range(4) if d_x in [0, 3] or d_y in [0, 3]],
        "EL_SHAPE_0": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)],   # No rotate, original shape
        "EL_SHAPE_90": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)],  # Rotated 90 degree
        "EL_SHAPE_180": [(3, 0), (3, 1), (3, 2), (3, 3), (0, 3), (1, 3), (2, 3)], # Rotated 180 degree
        "EL_SHAPE_270": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]  # Rotated 270 degree
    }
    
    pattern = tile_patterns[tile_shape]  # Get the tile pattern for the given "tile_shape"
    max_row = len(landscape)
    max_col = len(landscape[0]) if max_row > 0 else 0
    
    # Check if the tile goes out of boundary or see if it overlaps with another tile
    for d_x, d_y in pattern:
        x, y = position[0] + d_x, position[1] + d_y
        # Mark the tile position as "9" to indicate the tile covers this position
        if x < 0 or x >= max_row or y < 0 or y >= max_col or landscape[x][y] == 9:
            return False  # The tile goes out of bounds or overlaps another tile
    
    # See if there are tiles left to place
    base_tile_shape = tile_shape.split("_")[0] + "_" + tile_shape.split("_")[1]  # EL_SHAPE_90 -> EL_SHAPE
    # If there's no tile left, then you can't place anymore
    if tiles.get(base_tile_shape, 0) <= 0:
        return False

    return True  # The placement is valid under all constraints

def initialize_neighbors(variables, tile_size, landscape_size):
    """
    Define the neighbors.
    """
    neighbors = {}
    
    for x_i in variables:
        x_i_neighbors = set()
        # To see neighbors, try to find all possible positions around "x_i"
        for d_x in [-tile_size, 0, tile_size]:
            for d_y in [-tile_size, 0, tile_size]:
                # excluding "x_i" itself
                if d_x == 0 and d_y == 0:
                    continue
                neighbor_position = (x_i[0] + d_x, x_i[1] + d_y)
                # Check if the neighbor is in variables, and check if it's within the size of the landscape
                if neighbor_position in variables and 0 <= neighbor_position[0] < landscape_size and 0 <= neighbor_position[1] < landscape_size:
                    x_i_neighbors.add(neighbor_position)
        neighbors[x_i] = x_i_neighbors
        
    return neighbors

def initialize_arcs(variables):
    """
    Define the arcs.
    """
    arcs = []
    
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            arcs.append((variables[i], variables[j]))
            arcs.append((variables[j], variables[i]))  # Ensure the symmetry!
            
    return arcs

def ac3(csp):
    """
    The AC3 algorithm for constraint propagation (Algorithm based on the PPT slide).
    Initialize queue with all arcs in the CSP. For each arc, check for consistency
    and prune domain values, if needed. Repeat this until no more pruning is possible
    or inconsistency is found.
    """
    queue = deque(csp["arcs"])           # Queue of all arcs, csp["arcs"] is a list of all arcs
    while queue:
        (x_i, x_j) = queue.popleft()     # Arc from "x_i" to "x_j"
        if revise(csp, x_i, x_j):
            if not csp["domains"][x_i]:  # If the domain of "x_i" is empty, there is no solution
                return False
            for x_k in (csp["neighbors"][x_i] - {x_j}):
                queue.append((x_k, x_i)) # Add neighboring arcs back to the queue
    return True

def revise(csp, x_i, x_j):
    """
    AC3 algirithm's helper function.
    """
    # "domains" is a dict with variables as keys and sets of values as domains
    revised = False
                
    for x in set(csp["domains"][x_i]):  # Create a copy to iterate over since we modify the domain
        # Check if the placement of "x" at "x_i" violates any constraints
        # Need to assume "is_valid" checks for all necessary constraints
        if "EL_SHAPE" in x:  # Consider all directions of EL_SHAPE's rotation
            valid = False
            for rotation in ["0", "90", "180", "270"]:  # All possible rotations
                tile_shape = f"{x}_{rotation}"          # "EL_SHAPE_0", "EL_SHAPE_90", etc...
                if is_valid(csp["landscape"], tile_shape, x_i, csp["tiles"]):
                    valid = True
                    break
            if not valid:
                if x in csp["domains"][x_i]:
                    csp["domains"][x_i].remove(x)
                    revised = True                
        else:
            if not is_valid(csp["landscape"], x, x_i, csp["tiles"]):
                if x in csp["domains"][x_i]:
                    csp["domains"][x_i].remove(x)
                    revised = True
        
    return revised

def backtrack(assignment, csp, original_numbers):
    """
    The most important one: Backtracking search algorithm. It will use MRV and LCV here.
    """
    if len(assignment) == len(csp["variables"]):
        # Check for the visibility of bushes
        visible_bushes = {bush: 0 for bush in csp["targets"]}
        for i, row in enumerate(csp["landscape"]):
            for j, cell in enumerate(row):
                if cell in csp["targets"]:
                    visible_bushes[cell] += 1
                    
        print("Updating --- Landscape:", print([print(row) for row in csp["landscape"]]))
        print("Updating --- Visible Bushes(Targets):", visible_bushes)
                    
        # See if they are all correct(True)
        all_correct_visible_bushes = all(visible_bushes[bush] == csp["targets"][bush] for bush in csp["targets"])
        if all_correct_visible_bushes:
            print("COMPLETED! --- Landscape:", print([print(row) for row in csp["landscape"]]))
            print("COMPLETED! --- Visible Bushes(Targets):", visible_bushes)
            return assignment  # Return the assignment successfully
        
        return None

    var = select_unassigned_tile_spot(csp, assignment, original_numbers)            # Tile positions
    for tile_shape in order_domain_values(var, assignment, csp, original_numbers):  # Each tile shape from the Tile Patterns (value) is in the order
        if is_valid(csp["landscape"], tile_shape, var, csp["tiles"]):
            apply_tile(csp['landscape'], tile_shape, var, csp["tiles"], original_numbers)
            assignment[var] = tile_shape  # This will be the final tile assignment at the end for each position
            result = backtrack(assignment, csp, original_numbers)
            if result is not None:
                return result
            remove_tile(csp["landscape"], tile_shape, var, csp["tiles"], original_numbers)
            del assignment[var]
    
    return None

def select_unassigned_tile_spot(csp, assignment, original_numbers):
    """
    Minimum Remaining Values(MRV) heuristic, with Tie-Breaking Rules.
    Choose a tile spot(variable) with the MRV in its domain that is not yet assigned.
    """
    # Variables that have not yet been assigned in the current assignment
    unassigned_variables = [v for v in csp["variables"] if v not in assignment]
    
    # Initialize the variable to return and its count of remaining values
    min_variable = None
    min_count = float("inf")
    least_constraints = float("inf")  # For Tie-Breaking Rules, least constraints
            
    for variable in unassigned_variables:
        # Count the number of legal values remaining for this variable
        count = 0
        local_least_constraints = float("inf")  # For tracking the least constraints for the current variable
        
        for base_tile_shape in csp["tiles"].keys():
            if "EL_SHAPE" in base_tile_shape:                     # Consider all directions of EL_SHAPE's rotation
                for rotation in ["0", "90", "180", "270"]:        # All possible rotations
                    tile_shape = f"{base_tile_shape}_{rotation}"  # "EL_SHAPE_0", "EL_SHAPE_90", etc...
                    if csp["tiles"][base_tile_shape] > 0 and is_valid(csp["landscape"], tile_shape, variable, csp["tiles"]):
                        count += 1
                        # Calculate constraints for this tile placement
                        constraints = count_constraints(csp["landscape"], tile_shape, variable, csp["variables"], assignment, csp["tiles"], original_numbers)
                        local_least_constraints = min(local_least_constraints, constraints)
            else:
                # If it's not the "EL_SHAPE", and not rotatable
                if csp["tiles"][base_tile_shape] > 0 and is_valid(csp["landscape"], base_tile_shape, variable, csp["tiles"]):
                    count += 1
                    # Calculate constraints for this tile placement
                    constraints = count_constraints(csp["landscape"], base_tile_shape, variable, csp["variables"], assignment, csp["tiles"], original_numbers)
                    local_least_constraints = min(local_least_constraints, constraints)
                
        # Minimum Remaining Values(MRV) heuristic
        if count < min_count:
            min_count = count
            min_variable = variable
            least_constraints = local_least_constraints  # Update least_constraints for Tie-Breaking Rules
        # When there are the same MRV, apply the Tie-Breaking Rules
        elif count == min_count and local_least_constraints < least_constraints:
            min_count = count
            min_variable = variable
            least_constraints = local_least_constraints
    
    return min_variable

def order_domain_values(position, assignment, csp, original_numbers):
    """
    Least Constraining Value(LCV) heuristic.
    For each tile shape, calculate the number of constraints with the count_constraints() function and sort the values based on the results.
    This arranges each tile shape in the order of the few constraints it imposes on the other variables.
    """
    # "tile_shape"s are the keys of "tiles", and the values are the count of how many tiles left
    
    values = []
    
    for base_tile_shape in csp["tiles"].keys():
        if "EL_SHAPE" in base_tile_shape:                     # Consider all directions of EL_SHAPE's rotation
            for rotation in ["0", "90", "180", "270"]:        # All possible rotations
                tile_shape = f"{base_tile_shape}_{rotation}"  # "EL_SHAPE_0", "EL_SHAPE_90", etc...
                if csp["tiles"][base_tile_shape] > 0:
                    # Calculate the constraint for this tile placement
                    constraints= count_constraints(csp["landscape"], tile_shape, position, csp["variables"], assignment, csp["tiles"], original_numbers)
                    values.append((tile_shape, constraints))
        else:
            # If it's not the "EL_SHAPE", and not rotatable
            if csp["tiles"][base_tile_shape] > 0:
                # Calculate the constraint for this tile placement
                constraints = count_constraints(csp["landscape"], base_tile_shape, position, csp["variables"], assignment, csp["tiles"], original_numbers)
                values.append((base_tile_shape, constraints))
                                            
    # Sort the tiles based on the number of constraints they impose, which means the least constraints first
    values.sort(key=lambda x: x[1])

    # Get the sorted list of the tile shapes
    sorted_tile_shapes = [tile for tile, _ in values]
    
    return sorted_tile_shapes

def count_constraints(landscape, tile_shape, position, variables, assignment, tiles, original_numbers):
    """
    A Helper function for both MRV and LCV heuristics to count how many constraints a tile choice
    imposes on other variables. For simplicity, we count the number of places a tile cannot be
    placed as a result of choosing this tile_shape at this position.
    """
    constraints = 0
    
    apply_tile(landscape, tile_shape, position, tiles, original_numbers)  # "Hypothetically" place the tile
    
    for variable in variables:
        if variable not in assignment:
            if "EL_SHAPE" in tile_shape:                             # Consider all directions of EL_SHAPE's rotation
                for rotation in ["0", "90", "180", "270"]:           # All possible rotations
                    rotated_tile_shape = f"{tile_shape}_{rotation}"  # "EL_SHAPE_0", "EL_SHAPE_90", etc...
                    if tiles.get(tile_shape, 0) > 0 and not is_valid(landscape, rotated_tile_shape, variable, tiles):
                        constraints += 1
            else:
                # If it's not EL_SHAPE, no consideration for rotation
                if tiles.get(tile_shape, 0) > 0 and not is_valid(landscape, tile_shape, variable, tiles):
                    constraints += 1
                    
    remove_tile(landscape, tile_shape, position, tiles, original_numbers)  # Remove the "hypothetical" tile
    
    return constraints


if __name__ == "__main__":
    # Read the tiles problem input file
    landscape, tiles, targets, _ = read_input_file(
        "Option 3_Tile Placement/tileplacement/withAnswerKeys/tilesproblem_1326658913086500.txt")  # Change the input file if needed.
        # "Option 3_Tile Placement/tileplacement/withAnswerKeys/tilesproblem_1326658934155700.txt")  # Change the input file if needed.
    
    # Assume landscape should be a "square" shape, and each tile must be a "4x4" size
    # and landscape is a list of lists representing the grid
    tile_size = 4
    landscape_size = len(landscape)
    variables = [(i, j) for i in range(0, landscape_size, tile_size)  # Each position that tiles can be placed accordingly
                    for j in range(0, landscape_size, tile_size)]
    neighbors = initialize_neighbors(variables, tile_size, landscape_size)
    
    original_numbers = {}  # Stores the original numbers that was on the landscape during tile placement
    original_num_tiles = copy.deepcopy(tiles)  # Deep copy the original "tiles"
    
    # Assume "tiles" contains the types(shapes) of tiles as keys
    tile_shapes = list(tiles.keys())  # Should contain the tile shapes, ex. ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']

    # Initialize domains for each variable (position)
    domains = {variable: tile_shapes for variable in variables}

    csp = {
        "landscape": landscape,
        "tiles": tiles,
        "targets": targets,
        "variables": variables,
        "arcs": initialize_arcs(variables),  # csp["arcs"] is a list of tuples (x_i, x_j), and each tuple means an arc from x_i to x_j
        "neighbors": neighbors,
        "domains": domains                   # csp["domains"] is a dict with variables as keys and sets of values as domains
    }
    
    # Apply AC3 algorithm to reduce domains before starting backtracking
    if ac3(csp):
        assignment = {}
        solution = backtrack(assignment, csp, original_numbers)
        print("COMPLETED! --- Tiles:", original_num_tiles)
        if solution is not None:
            print("Solution found!\n>>>>>\n", solution)
        else:
            print("*****NO solution exists!*****")
    else:
        print("*****ALERT: NO solution can be found!*****")
        