import numpy as np
cimport numpy as np


cpdef tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]] split_train_test(
    np.ndarray x, np.ndarray y, double train_percentage, bint sequential=*
) except *


cpdef tuple[np.ndarray, np.ndarray] create_window(
    np.ndarray data, int window_size
) except *
