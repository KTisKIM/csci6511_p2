###########################################
###                                     ###
###     Name: Keuntae Kim               ###
###     GWID: G30341718                 ###
###     CSCI 6511(AI) - Online          ###
###     Project 2: CSP                  ###
###     Option: 3. Tile Placement       ###
###                                     ###
###########################################

from collections import deque


def read_input_file(filename):
    """
    Reads Landscape, Tiles, Targets, and Solution Key(if needed) from the input file
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
            if line.startswith("# Landscape"):  ### Landscape Title
                read_landscape = True
            elif line.startswith("# Tiles:"):  ### Tiles Title
                if read_solution_key != True:
                    read_landscape = False
                    read_tiles = True
                elif read_solution_key == True:  # To filter out the solution key's tiles
                    # print("This is the Solution Key's Tiles.")
                    None
                else:
                    print("ERROR: It's reading something wrong!")
            elif line.startswith("# Targets:"):  ### Targets Title
                read_tiles = False
                read_targets = True
            elif line.startswith("# Tiles Problem Solution Key"):  ### Solution Key Title (if needed for testing)
                read_targets = False
                read_solution_key = True
                
            elif line and read_landscape:  ### Landscape
                was_previous_empty = False  # Initialize: check if previous item was empty
                for number in line.split(" "):
                    if number.isdigit():  # When it's a number
                        list_current_line.append(int(number))
                        was_previous_empty = False
                    else:  # when it's an empty space
                        if not was_previous_empty:  # if previous was not empty space, this is the first empty
                            was_previous_empty = True
                        elif number == "":
                            list_current_line.append(0)  # "0" here shows the empty spaces
                            was_previous_empty = False  # reset the status after taking care of consecutive empty space
                landscape.append(list_current_line)  # add the whole list(single line) to the landscape
            elif line and read_tiles:  ### Tiles
                tiles_list = line.strip("{}").split(", ")
                for tile in tiles_list:
                    tile_shape, tile_counts = tile.split("=")
                    tiles[tile_shape] = int(tile_counts)
            elif line and read_targets:  ### Targets
                bush, bush_counts = line.split(":")
                targets[int(bush)] = int(bush_counts)
            elif line and read_solution_key:  ### Solution Key (if needed for testing)
                tile_solution = line.split()
                index = int(tile_solution[0])
                tile_size = int(tile_solution[1])
                tile_shape = tile_solution[2]
                solution_key.append([index, tile_size, tile_shape])
            else:  ### No-needed lines. Doesn't do anything.
                # print("<< non defined >>")
                None
    
    ## To see if the function parsed the input file correctly
    # print("Landscape:\n", [print(row) for row in landscape])  # print statement appears above the "Landscape:" for some reason
    # print("Tiles:\n", tiles)
    # print("Targets:\n", targets)
    # print("Solution Key:\n", [print(index) for index in solution_key])  # print statement appears above the "Solution Key:" for some reason

    return landscape, tiles, targets, solution_key


def is_valid(landscape, tile_type, position, targets, tiles):
    """
    Check if placing a tile at position is valid(overlaps with any other existing tile?) according to the landscape and constraints,
    thus existing tile. This function considers the tile's shape, and check if the visibility of bushes
    after placing this tile still meets the target requirements.
    """
    # Define the patterns for each tile type in terms of offsets from the top-left corner
    tile_patterns = {
        "FULL_BLOCK": [(d_x, d_y) for d_x in range(4) for d_y in range(4)],
        "OUTER_BOUNDARY": [(d_x, d_y) for d_x in range(4) for d_y in range(4) if d_x in [0, 3] or d_y in [0, 3]],
        "EL_SHAPE_0": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)],  # No rotate, original state
        "EL_SHAPE_90": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)], # Rotate 90 degree
        "EL_SHAPE_180": [(3, 0), (3, 1), (3, 2), (3, 3), (0, 3), (1, 3), (2, 3)], # Rotate 180 degree
        "EL_SHAPE_270": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]  # Rotate 270 degree
    }
    
    pattern = tile_patterns[tile_type]  # Get the tile pattern for the given tile_type
    max_row = len(landscape)
    max_col = len(landscape[0]) if max_row > 0 else 0
    
    # Check landscape bounds and if the tile overlaps with other tiles or not
    for d_x, d_y in pattern:
        x, y = position[0] + d_x, position[1] + d_y
        if x >= max_row or y >= max_col or landscape[x][y] == 9:
            return False  # The tile goes out of bounds or overlaps another tile
        
    # Simulate tile placement to check visibility constraints
    # Creating a shallow copy of landscape rows to simulate tile placement
    simulate_landscape = [row[:] for row in landscape]
    for d_x, d_y in pattern:
        x, y = position[0] + d_x, position[1] + d_y
        # Mark the tile position as '9' to indicate the tile covers this area
        if 0 <= x < max_row and 0 <= y < max_col:
            simulate_landscape[x][y] = 9
    # print("맵을 좀 봐봐", [print(i) for i in simulate_landscape])  #TODO
    
    # Calculate visible bushes after simulated tile placement
    visible_bushes = {bush: 0 for bush in targets}
    for i, row in enumerate(simulate_landscape):
        for j, cell in enumerate(row):
            if cell in targets:
                visible_bushes[cell] += 1
                # print("보이는 수", visible_bushes)  #TODO
    
    # Check if the simulated placement meets the visibility requirements
    for bush, num_visibility in targets.items():
        if visible_bushes[bush] != num_visibility:
            return False  # Placing the tile violates visibility requirements
        
    base_tile_type = tile_type.split("_")[0] + "_" + tile_type.split("_")[1]  # EL_SHAPE_90 -> EL_SHAPE
    # If there's no left tile, then you can't place anymore
    if tiles.get(base_tile_type, 0) <= 0:
        return False

    return True  # The placement is valid under all constraints

def apply_tile(landscape, tile_type, position, tiles, original_numbers):
    """
    Place the tile on the landscape and update visibility accordingly
    """
    # x, y = position  # x, y denote the top-left corner where the tile will be placed

    # Define the patterns for each tile type in terms of offsets from the top-left corner
    tile_patterns = {
        "FULL_BLOCK": [(d_x, d_y) for d_x in range(4) for d_y in range(4)],
        "OUTER_BOUNDARY": [(d_x, d_y) for d_x in range(4) for d_y in range(4) if d_x in [0, 3] or d_y in [0, 3]],
        "EL_SHAPE_0": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)],  # No rotate, original state
        "EL_SHAPE_90": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)], # Rotate 90 degree
        "EL_SHAPE_180": [(3, 0), (3, 1), (3, 2), (3, 3), (0, 3), (1, 3), (2, 3)], # Rotate 180 degree
        "EL_SHAPE_270": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]  # Rotate 270 degree
    }
    
    print("수정전타일", tiles)  #TODO
    # Get the pattern for the given tile_type
    pattern = tile_patterns.get(tile_type, [])
    
    # Apply the tile by setting the covered positions to a specific non-zero value
    for d_x, d_y in pattern:
        x, y = position[0] + d_x, position[1] + d_y
        # Check if the position is within the bounds of the landscape
        if 0 <= x < len(landscape) and 0 <= y < len(landscape[0]):
            original_numbers[(x, y)] = landscape[x][y]  # Store the original numbers that were in the positions
            landscape[x][y] = 9  # Assume '9' indicates the presence of a tile
            
    # Reduce the quantity of the corresponding tile type in tiles
    base_tile_type = tile_type.split("_")[0] + "_" + tile_type.split("_")[1]  # EL_SHAPE_90 -> EL_SHAPE
    tiles[base_tile_type] -= 1
    print("타일", tiles)  #TODO

def remove_tile(landscape, tile_type, position, tiles, original_numbers):
    """
    Remove the tile from the landscape, reverting visibility changes
    Basically, reverse the operation done by apply_tile()
    Make sure the landscape is reverted to its state before the tile was placed.
    """
    # Define the patterns for each tile type in terms of offsets from the top-left corner
    tile_patterns = {
        "FULL_BLOCK": [(d_x, d_y) for d_x in range(4) for d_y in range(4)],
        "OUTER_BOUNDARY": [(d_x, d_y) for d_x in range(4) for d_y in range(4) if d_x in [0, 3] or d_y in [0, 3]],
        "EL_SHAPE_0": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)],  # No rotate, original state
        "EL_SHAPE_90": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)], # Rotate 90 degree
        "EL_SHAPE_180": [(3, 0), (3, 1), (3, 2), (3, 3), (0, 3), (1, 3), (2, 3)], # Rotate 180 degree
        "EL_SHAPE_270": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]  # Rotate 270 degree
    }
    
    # Get the pattern for the given tile_type
    pattern = tile_patterns.get(tile_type, [])
    
    # Remove the tile by setting the covered positions back to what it was
    for d_x, d_y in pattern:
        x, y = position[0] + d_x, position[1] + d_y
        if (x, y) in original_numbers:
            landscape[x][y] = original_numbers[(x, y)]  # Revert it back to the original number
            del original_numbers[(x, y)]  # Delete the restored number from the orignal_numbers
        
    # Increase the quantity of the corresponding tile type in tiles
    base_tile_type = tile_type.split("_")[0] + "_" + tile_type.split("_")[1]  # EL_SHAPE_90 -> EL_SHAPE
    tiles[base_tile_type] += 1

    return landscape

def initialize_neighbors(variables, tile_size, landscape_size):
    neighbors = {}
    
    for x_i in variables:
        x_i_neighbors = set()
        # To see neighbors, try to find all possible positions around x_i
        for d_x in [-tile_size, 0, tile_size]:
            for d_y in [-tile_size, 0, tile_size]:
                # excluding x_i itself
                if d_x == 0 and d_y == 0:
                    continue
                neighbor_position = (x_i[0] + d_x, x_i[1] + d_y)
                # Check if the neighbor is in variables, and check if it is within the size of the landscape
                if neighbor_position in variables and 0 <= neighbor_position[0] < landscape_size and 0 <= neighbor_position[1] < landscape_size:
                    x_i_neighbors.add(neighbor_position)
        neighbors[x_i] = x_i_neighbors
        
    return neighbors

def initialize_arcs(variables):
    """
    Define the arcs
    """
    arcs = []
    
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            arcs.append((variables[i], variables[j]))
            arcs.append((variables[j], variables[i]))  # Ensure the symmetry!
            
    return arcs

def ac3(csp):  #TODO
    """
    The AC3 algorithm for constraint propagation. Initialize queue with all arcs in the CSP.
    For each arc, check for consistency and prune domain values, if needed.
    Repeat this until no more pruning is possible or inconsistency is found.
    """
    queue = deque(csp["arcs"])  # Queue of all arcs, assume csp["arcs"] is a list of all arcs
    while queue:
        (x_i, x_j) = queue.popleft()  # Arc from x_i to x_j
        if revise(csp, x_i, x_j):
            if not csp["domains"][x_i]:  # If the domain of x_i is empty, there is no solution
                return False
            for x_k in (csp["neighbors"][x_i] - {x_j}):
                queue.append((x_k, x_i))  # Add neighboring arcs back to the queue
    return True

def revise(csp, x_i, x_j):  #TODO
    # Assume that 'domains' is a dict with variables as keys and sets of values as domains
    revised = False
    
    # for x in set(csp["domains"][x_i]):  # Create a copy to iterate over since we might modify the domain
    #     # Check if the placement of `x` at `x_i` violates any constraints
    #     # Assume `is_valid` checks for all necessary constraints including interactions with other variables
    #     if not is_valid(csp["landscape"], x, x_i, csp["targets"], csp["tiles"]):
    #             csp["domains"][x_i].remove(x)
    #             revised = True
                
    for x in set(csp["domains"][x_i]):  # Create a copy to iterate over since we might modify the domain
        # Check if the placement of `x` at `x_i` violates any constraints
        # Assume `is_valid` checks for all necessary constraints including interactions with other variables
        print("디버그디버그디버그:", x, csp["domains"][x_i])  #TODO
        if "EL_SHAPE" in x:  # Consider all directions of rotation
            for rotation in ["0", "90", "180", "270"]:  # All Possible rotations
                tile_type = f"{x}_{rotation}"  # "EL_SHAPE_0", "EL_SHAPE_90", etc...
                if not is_valid(csp["landscape"], tile_type, x_i, csp["targets"], csp["tiles"]):  # TODO, 여기 해결해야 함.
                    if len(csp["domains"][x_i]) == 0:
                        break
                    csp["domains"][x_i].remove(x)
                    revised = True
        else:
            if len(csp["domains"][x_i]) == 0:
                break
            if not is_valid(csp["landscape"], x, x_i, csp["targets"], csp["tiles"]):  # TODO, 여기도 마찬가지로 해결해야 함.
                csp["domains"][x_i].remove(x)
                revised = True
        
    return revised

def backtrack(assignment, csp, original_numbers):
    """
    Backtracking search algorithm. It will use MRV and LCV
    """
    if len(assignment) == len(csp["variables"]):
        return assignment  # Return the assignment successfully

    var = select_unassigned_variable(csp, assignment, original_numbers)
    for value in order_domain_values(var, assignment, csp, original_numbers):            
        print("디버그: 여기까지 왔다", value)  # TODO
        if is_valid(csp["landscape"], value, var, csp["targets"], csp["tiles"]):  # TODO, 이거 해결해야 함.
            print("여기까지 왔어!!! for루프 안쪽 if문 안쪽!")  #TODO
            apply_tile(csp['landscape'], value, var, csp["tiles"], original_numbers)
            assignment[var] = value
            result = backtrack(assignment, csp, original_numbers)
            if result is not None:
                return result
            remove_tile(csp["landscape"], value, var, csp["tiles"], original_numbers)
            del assignment[var]
    return None

def select_unassigned_variable(csp, assignment, original_numbers):
    """
    MRV heuristic. Choose a variable with the Minimum Remaining Values in its domain that is not yet assigned.
    """
    unassigned_variables = [v for v in csp["variables"] if v not in assignment]  # variables that have not yet been assigned in the current assignment
    # Initialize the variable to return and its count of remaining values
    min_variable = None
    min_count = float("inf")
    least_constraints = float("inf")  # For Tie-Breaking Rules, least constraints
            
    for variable in unassigned_variables:
        # Count the number of legal values remaining for this variable
        count = 0
        local_least_constraints = float("inf")  # For tracking the least constraints for the current variable
        
        for base_tile_type in csp["tiles"].keys():
            if "EL_SHAPE" in base_tile_type:  # Consider all directions of rotation
                for rotation in ["0", "90", "180", "270"]:  # All Possible rotations
                    tile_type = f"{base_tile_type}_{rotation}"  # "EL_SHAPE_0", "EL_SHAPE_90", etc...
                    if csp["tiles"][base_tile_type] > 0 and is_valid(csp["landscape"], tile_type, variable, csp["targets"], csp["tiles"]):  # TODO, 여기도 해결해야.
                        count += 1
                        # Calculate constraints for this tile placement
                        constraints = count_constraints(csp["landscape"], tile_type, variable, csp["variables"], assignment, csp["tiles"], csp["targets"], original_numbers)
                        local_least_constraints = min(local_least_constraints, constraints)
            else:
                # If it's not EL_SHAPE (not rotatable)
                if csp["tiles"][base_tile_type] > 0 and is_valid(csp["landscape"], base_tile_type, variable, csp["targets"], csp["tiles"]):  # TODO, 여기도 해결해야.
                    count += 1
                    # Calculate constraints for this tile placement
                    constraints = count_constraints(csp["landscape"], base_tile_type, variable, csp["variables"], assignment, csp["tiles"], csp["targets"], original_numbers)
                    local_least_constraints = min(local_least_constraints, constraints)
                
        # MRV
        if count < min_count:
            min_count = count
            min_variable = variable
            # count_constraints(landscape, tile_type, position, variables, assignment, tiles, targets, original_numbers)
            least_constraints = local_least_constraints  # Update least_constraints for Tie-Breaking Rules
        # When there are the same MRV, apply the Tie-Breaking Rules
        elif count == min_count and local_least_constraints < least_constraints:
            min_count = count
            min_variable = variable
            least_constraints = local_least_constraints
    
    return min_variable

def order_domain_values(var, assignment, csp, original_numbers):
    """
    For LCV heuristic. For a given variable, order the values in its domain based on how many constraints they impose on other variables.
    """
    # Assume that "tiles" are the keys of tile types and the values are the count of how many tiles left
    values = []
    for base_tile_type in csp["tiles"].keys():
        if "EL_SHAPE" in base_tile_type:  # Consider all directions of rotation
            for rotation in ["0", "90", "180", "270"]:  # All Possible rotations
                tile_type = f"{base_tile_type}_{rotation}"  # "EL_SHAPE_0", "EL_SHAPE_90", etc...
                values.append(tile_type)
        else:
            # If it's not EL_SHAPE (not rotatable)
            values.append(base_tile_type)
    
    # with Tie-Breaking Rules
    order = sorted(values, key=lambda value: (count_constraints(csp["landscape"], value, var, csp["variables"], assignment, csp["tiles"], csp["targets"], original_numbers), # Number of constraints
                                              -csp["tiles"].get(value.split("_")[0], 0))) # Number of remaining tiles ("negative" numbers to sort in large order)
    
    return order

def count_constraints(landscape, tile_type, position, variables, assignment, tiles, targets, original_numbers):
    # A helper function to count how many constraints a tile choice imposes on other variables
    # For simplicity, we count the number of places a tile cannot be placed as a result of choosing this tile_type at this position
    constraints = 0
    
    apply_tile(landscape, tile_type, position, tiles, original_numbers)  # Hypothetically place the tile
    
    for variable in variables:
        if variable not in assignment:
            if "EL_SHAPE" in tile_type:
                for rotation in ["0", "90", "180", "270"]:  # All Possible rotations
                    rotated_tile_type = f"{tile_type}_{rotation}"  # "EL_SHAPE_0", "EL_SHAPE_90", etc...
                    # Consider all directions of rotation
                    if tiles.get(tile_type, 0) > 0 and not is_valid(landscape, rotated_tile_type, variable, targets, tiles):  # TODO, 여기도 해결해야.
                        constraints += 1
            else:
                # If it's not EL_SHAPE, no consideration for rotation
                if tiles.get(tile_type, 0) > 0 and not is_valid(landscape, tile_type, variable, targets, tiles):  # TODO, 여기도 해결해야.
                    constraints += 1
                    
    remove_tile(landscape, tile_type, position, tiles, original_numbers)  # Remove the hypothetical tile
    
    return constraints


if __name__ == "__main__":
    landscape, tiles, targets, _ = read_input_file(
        "Option 3_Tile Placement/tileplacement/withAnswerKeys/tilesproblem_1326658913086500.txt")  # Change the input file if needed.
    
    # Assume landscape is a "square" and each tile is "4x4"
    tile_size = 4
    landscape_size = len(landscape)  # Assume landscape is a list of lists representing the grid
    variables = [(i, j) for i in range(0, landscape_size, tile_size)
                    for j in range(0, landscape_size, tile_size)]
    neighbors = initialize_neighbors(variables, tile_size, len(landscape))
    
    # # Define the patterns for each tile type in terms of offsets from the top-left corner
    # tile_patterns = {
    #     "FULL_BLOCK": [(d_x, d_y) for d_x in range(4) for d_y in range(4)],
    #     "OUTER_BOUNDARY": [(d_x, d_y) for d_x in range(4) for d_y in range(4) if d_x in [0, 3] or d_y in [0, 3]],
    #     "EL_SHAPE_0": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)],  # No rotate, original state
    #     "EL_SHAPE_90": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)], # Rotate 90 degree
    #     "EL_SHAPE_180": [(3, 0), (3, 1), (3, 2), (3, 3), (0, 3), (1, 3), (2, 3)], # Rotate 180 degree
    #     "EL_SHAPE_270": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]  # Rotate 270 degree
    # }  # Instead, plugged it into each function who needs this
    
    original_numbers = {}  # Stores the original number during tile placement
    
    # Assume 'tiles' contains the types of tiles as keys
    tile_types = list(tiles.keys())  # This list should contain your tile types, ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']

    # Initialize domains for each variable (position)
    domains = {variable: tile_types for variable in variables}

    csp = {
        "landscape": landscape,
        "tiles": tiles,
        "targets": targets,
        "variables": variables,
        "arcs": initialize_arcs(variables),  # csp["arcs"] is a list of tuples (x_i, x_j), and each tuple means an arc from x_i to x_j
        "neighbors": neighbors,
        "domains": domains  # csp["domains"] is a dict with variables as keys and sets of values as domains
    }
    
    # Apply AC3 algorithm to reduce domains before starting backtracking
    if ac3(csp):
        assignment = {}
        solution = backtrack(assignment, csp, original_numbers)
        if solution is not None:
            print("Solution found:", solution)
        else:
            print("No solution exists.")
    else:
        print("No solution can be found.")
        