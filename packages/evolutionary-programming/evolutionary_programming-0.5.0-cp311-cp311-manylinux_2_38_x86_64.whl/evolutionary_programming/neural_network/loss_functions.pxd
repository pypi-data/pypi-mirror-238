import numpy as np
cimport numpy as np
from numpy cimport ndarray


ctypedef ndarray (*LossFunction)(ndarray, ndarray, bint) except *


cdef dict[str, LossFunction] LOSS_FUNCTIONS


cdef ndarray neg_log_likelihood(ndarray y, ndarray y_hat, bint derivative) except *


cdef ndarray softmax_neg_log_likelihood(ndarray y, ndarray y_hat, bint derivative) except *


cdef ndarray mae(ndarray y, ndarray y_hat, bint derivative) except *


cdef ndarray mse(ndarray y, ndarray y_hat, bint derivative) except *


cdef ndarray rmse(ndarray y, ndarray y_hat, bint derivative) except *
