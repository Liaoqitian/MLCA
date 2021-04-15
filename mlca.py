def generate(center_cell, max_state, survive_arr, born_arr):
    live_cells_count = np.sum((neighborhood == max_state).astype(int))
        if center_cell == max_state: 
            for num_neighbors in survive_arr:
                if live_cells_count - 1 == num_neighbors: 
                    return center_cell 
            return center_cell – 1
        else if center_cell != 0 and center_cell != max_state:
            return center_cell – 1
        else:
            for num_neighbors in born_arr: 
                if total == num_neighbors:
                    return max_state 
            return 0
