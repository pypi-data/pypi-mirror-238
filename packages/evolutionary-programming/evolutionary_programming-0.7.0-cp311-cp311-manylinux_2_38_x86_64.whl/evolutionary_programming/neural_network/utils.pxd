from numpy cimport ndarray


ctypedef ndarray (*WeightInitializer)(int, int) except *


cdef dict[str, WeightInitializer] WEIGHT_INITIALIZERS


cdef ndarray ones_initializer(int rows, int cols) except *


cdef ndarray zeros_initializer(int rows, int cols) except *


cdef ndarray random_uniform_initializer(int rows, int cols) except *


cdef ndarray glorot_uniform_initializer(int rows, int cols) except *


cdef ndarray glorot_normal_initializer(int rows, int cols) except *


