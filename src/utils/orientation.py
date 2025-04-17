def choose_orientation(tokens: list[str], density_data: dict, translate_orientation: dict) -> list[int]:
    orientations = []
    previous_dense_above_dir = None
    previous_num_quarters_occupying = None

    for i, token in enumerate(tokens):
        if i == 0:
        # Only need to record dense above direction as is. The first token is never rotated.
            previous_dense_above_dir: list[str] = density_data[token]['dense_above_dir']
            previous_num_quarters_occupying: int = density_data[token]['quarters']
            orientations.append(0)
            continue
    
    # Have a temporary orientation which starts where the previous ripple ended
        temp_orientation = (orientations[i-1] + previous_num_quarters_occupying) % 4
    
    # CHOOSE ORIENTATION BASE ON DENSITY
    # Where it is dense below, it must not coincide with where the previous one is dense above
        dense_below_dir: list[str] = density_data[token]['dense_below_dir']
        chosen_orientation = 0
        for orientation in range(4):
            temp_dense_below_dir = [translate_orientation[str((orientation + temp_orientation) % 4)][d] for d in dense_below_dir]
        
        # Check intersection. Assumes orientation choices have been taken into consideration
            common_dirs = set(temp_dense_below_dir).intersection(set(previous_dense_above_dir))
            if not common_dirs:
            # No clash, valid orientation found
                chosen_orientation = (orientation + temp_orientation) % 4
                break
    
        orientations.append(chosen_orientation)
    
    # Keep information to help next token orientation
        previous_dense_above_dir = [translate_orientation[str(chosen_orientation)][d] for d in density_data[token]['dense_above_dir']]
        previous_num_quarters_occupying: int = density_data[token]['quarters']
    
    return orientations