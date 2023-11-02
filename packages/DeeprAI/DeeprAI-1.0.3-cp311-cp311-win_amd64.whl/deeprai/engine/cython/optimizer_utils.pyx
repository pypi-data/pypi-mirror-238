import numpy as np
from optimizers import *
from deeprai.engine.base_layer import  WeightVals, BiasVals

cdef dict momentum_initializer():
    return {
        "weight_velocity": [np.zeros_like(w) for w in WeightVals.Weights],
        "bias_velocity": [np.zeros_like(b) for b in BiasVals.Biases]
    }

cdef dict adagrad_initializer():
    return {
        "weight_accumulated_grad": [np.zeros_like(w) for w in WeightVals.Weights],
        "bias_accumulated_grad": [np.zeros_like(b) for b in BiasVals.Biases]
    }

cdef dict adadelta_initializer():
    return {
        "weight_accumulated_grad": [np.zeros_like(w) for w in WeightVals.Weights],
        "weight_accumulated_delta": [np.zeros_like(w) for w in WeightVals.Weights],
        "bias_accumulated_grad": [np.zeros_like(b) for b in BiasVals.Biases],
        "bias_accumulated_delta": [np.zeros_like(b) for b in BiasVals.Biases]
    }

cdef dict rmsprop_initializer():
    return {
        "weight_v": [np.zeros_like(w) for w in WeightVals.Weights],
        "bias_v": [np.zeros_like(b) for b in BiasVals.Biases]
    }

cdef dict adam_initializer():
    return {
        "weight_m": [np.zeros_like(w) for w in WeightVals.Weights],
        "weight_v": [np.zeros_like(w) for w in WeightVals.Weights],
        "bias_m": [np.zeros_like(b) for b in BiasVals.Biases],
        "bias_v": [np.zeros_like(b) for b in BiasVals.Biases],
        "t": 0
    }

optimizer_initializers = {
    "momentum": momentum_initializer,
    "adagrad": adagrad_initializer,
    "adadelta": adadelta_initializer,
    "rmsprop": rmsprop_initializer,
    "adam": adam_initializer
}

optimizer_updaters = {
    "gradient descent": gradient_descent_update,
    "momentum": momentum_update,
    "adagrad": adagrad_update,
    "adadelta": adadelta_update,
    "rmsprop": rmsprop_update,
    "adam": adam_update
}