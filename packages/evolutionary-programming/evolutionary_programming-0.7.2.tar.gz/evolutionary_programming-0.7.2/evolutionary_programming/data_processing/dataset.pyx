import numpy as np
cimport numpy as np


cpdef tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]] split_train_test(
    np.ndarray x, np.ndarray y, double train_percentage, bint sequential=True
) except *:
    # calculate the size of the sets
    data_size = len(x)
    train_size = int(train_percentage * data_size)

    # generate indices
    if sequential:
        train_indices = np.array(range(train_size))
        test_indices = np.array(range(train_size, data_size))
    else:
        train_indices = np.random.choice(
            range(data_size), size=train_size, replace=False
        )
        test_indices = np.array(
            [i for i in range(data_size) if i not in train_indices]
        )

    return (
        (x[train_indices], y[train_indices]),
        (x[test_indices], y[test_indices]),
    )


cpdef tuple[np.ndarray, np.ndarray] create_window(
    np.ndarray data, int window_size
) except *:
    x_data, y_data = [], []
    dataset_size = len(data)

    for i in range(dataset_size):
        # check if there is enough data
        if i + window_size + 1 > dataset_size:
            break

        # append data
        x_data.append(data[i: i + window_size])
        y_data.append(data[i + window_size])

    # convert to numpy array
    x_np = np.array(x_data)
    y_np = np.array(y_data)

    # fix array dimensions
    if x_np.ndim > 2:
        x_np = x_np.squeeze()
    if y_np.ndim > 2:
        y_np = y_np.squeeze()

    return (x_np, y_np)
