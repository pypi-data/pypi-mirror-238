import numpy as np    
        
def rand_col_seg(seg) -> np.ndarray:
    
    vals = np.unique(seg)
    colors = np.random.uniform(0.1, 1, (vals.max()+1, 3))
    colors[0] = [0, 0, 0]

    return colors[seg]
        