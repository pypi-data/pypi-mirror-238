import numpy as np
cimport numpy as np


cdef extern from "limits.h":
    const int INT_MAX


cdef extern from "float.h":
    const double DBL_MAX


cdef class DenseLayer:
    cdef public np.ndarray _weights
    cdef public np.ndarray _biases
    cdef public np.ndarray _gamma
    cdef public np.ndarray _beta

    # hyper params
    cdef public str _activation
    cdef public object _activation_fn
    cdef public str _regularization
    cdef public object _regularization_fn
    cdef public double _regularization_strength
    cdef public double _dropout_probability
    cdef public double _batch_decay
    cdef public bint _batch_norm

    # intermediary values
    cdef public np.ndarray _input
    cdef public np.ndarray _dropout_mask
    cdef public np.ndarray _activation_input
    cdef public np.ndarray _activation_output
    cdef public np.ndarray _dweights
    cdef public np.ndarray _dbias
    cdef public np.ndarray _dgamma
    cdef public np.ndarray _dbeta
    cdef public np.ndarray _prev_dweights
    cdef public np.ndarray _population_mean
    cdef public np.ndarray _population_var
    cdef public list _batch_norm_cache

cdef class NeuralNetwork:
    cdef public list _layers
    cdef public list _best_model
    cdef public double _learning_rate
    cdef public double _lr_decay_rate
    cdef public int _lr_decay_steps
    cdef public double _momentum
    cdef public int _patience
    cdef public double _best_loss
    cdef str _lr_decay
    cdef str _loss_function
    cdef object _lr_decay_fn
    cdef object _loss_function_fn
    cdef int _waiting
    cdef dict _initial_settings

    cdef np.ndarray _feedforward(self, np.ndarray x, bint training=*) except *
    cdef np.ndarray _backpropagation(self, np.ndarray y, np.ndarray y_hat) except *
    cdef void _restore_initial_settings(self) noexcept
    cpdef void add_layer(self, layer) except *
    cpdef double evaluate(self, np.ndarray x, np.ndarray y, str loss_name=*) except *
    cpdef np.ndarray predict(self, np.ndarray x) except *
    cpdef void save(self, str file_path) except *
    cpdef void fit(self, np.ndarray x_train, np.ndarray y_train, np.ndarray x_val=*,
        np.ndarray y_val=*, int epochs=*, object batch_generator=*,
        int batch_size=*, int verbose=*) except *

cdef np.ndarray _batch_normalization_forward(DenseLayer layer, np.ndarray x, bint training=*) except *


cdef np.ndarray _batch_normalization_backward(DenseLayer layer, np.ndarray dactivation) except *


cpdef NeuralNetwork _rebuild_neural_network(
    double learning_rate, str lr_decay, double lr_decay_rate, int lr_decay_steps,
    str loss_function, double momentum, int patience, list[DenseLayer] layers
) except *


cpdef DenseLayer _rebuild_dense_layer(
    int input_size, int output_size,
    str activation,
    str regularization, double regularization_strength,
    double dropout_probability,
    bint batch_norm,
    double batch_decay,
    np.ndarray weights, np.ndarray biases, np.ndarray gamma, np.ndarray beta
) except *
