from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np

from .state_vector_simulator import StateVectorSimulator

Tensor = Any


class NumpyBackend(StateVectorSimulator):
    def as_tensor(self, tensor: Tensor) -> Tensor:
        return np.asarray(tensor)

    def get_zero_state(self, qnum: int) -> Tensor:
        state = np.zeros(1 << qnum, dtype=complex)
        state[0] = 1
        return state

    def reshape(self, state: Tensor, shape: Sequence) -> Tensor:
        return np.reshape(state, shape)

    def ravel(self, state: Tensor) -> Tensor:
        return np.ravel(state)

    def stack(self, states: Sequence[Tensor], axis: int = 0) -> Tensor:
        return np.stack(states, axis=axis)

    def real(self, state: Tensor) -> Tensor:
        return np.real(state)

    def sum(self, state: Tensor, axis: int | None = None) -> Tensor:
        return np.sum(state, axis=axis)

    def conj(self, state: Tensor) -> Tensor:
        return np.conj(state)

    def sqrt(self, state: Tensor) -> Tensor:
        return np.sqrt(state)

    def copy(self, state: Tensor) -> Tensor:
        return state.copy()

    def dot(self, state1: Tensor, state2: Tensor) -> Tensor:
        return np.dot(state1, state2)
