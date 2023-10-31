import numpy as np
cimport numpy as np


cdef bint is_float(str string) noexcept


cdef string_to_csv_and_numpy(
    str input_string, str delimiter=*,
    bint header=*, int skiprows=*
) noexcept


cpdef list[np.ndarray] fetch_csv_to_numpy(
    str csv_url, list[int] columns=*, str delimiter=*,
    bint header=*,int skiprows=*,
) except *
