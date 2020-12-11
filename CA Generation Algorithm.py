if center_cell == max_state: 
	for num_neighbors in survive_arr:
		if total - 1 == num_neighbors: 
			return center_cell
	return center_cell - 1
elif center_cell != 0 and center_cell != max_state:
	return center_cell - 1
else:
	for num_neighbors in born_arr:
		if total == num_neighbors: 
			return max_state 
	return 0