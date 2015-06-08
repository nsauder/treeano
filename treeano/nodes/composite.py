"""
nodes which are combinations of multiple other nodes
"""

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import numpy as np
import theano
import theano.tensor as T

from .. import core
from . import simple
from . import containers


def _flatten_1d_or_2d(v):
    if v.ndim > 2:
        return T.flatten(v, outdim=2)
    elif 1 <= v.ndim <= 2:
        return v
    else:
        raise ValueError


def _flatten_1d_or_2d_shape(shape):
    if len(shape) > 2:
        return (shape[0], np.prod(shape[1:]))
    elif 1 <= len(shape) <= 2:
        return shape
    else:
        raise ValueError


@core.register_node("dense")
class DenseNode(core.WrapperNodeImpl):

    """
    applies a dense neural network layer to the input
    """

    children_container = core.NoneChildrenContainer
    hyperparameter_names = ("num_units",
                            "shared_initializations",
                            "initializations",
                            "inits")

    def architecture_children(self):
        return [
            containers.SequentialNode(
                self._name + "_sequential",
                [simple.ApplyNode(self._name + "_flatten",
                                  fn=_flatten_1d_or_2d,
                                  shape_fn=_flatten_1d_or_2d_shape),
                 simple.LinearMappingNode(self._name + "_linear"),
                 simple.AddBiasNode(self._name + "_bias")
                 ])]

    def get_hyperparameter(self, network, name):
        if name == "output_dim":
            # remap a child looking for "output_dim" to "num_units"
            return network.find_hyperparameter(["num_units"])
        else:
            return super(DenseNode, self).get_hyperparameter(network, name)