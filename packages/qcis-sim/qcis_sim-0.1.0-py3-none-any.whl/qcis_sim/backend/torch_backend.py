from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .state_vector_simulator import StateVectorSimulator

try:
    import torch

    torch_dtype = torch.complex64
except Exception:
    # pytorch is an optional backend
    torch_dtype = None


Tensor = Any


class TorchBackend(StateVectorSimulator):
    def __init__(self, topo: bool = True, dtype=None) -> None:
        super().__init__(topo=topo)
        if dtype is None:
            self.dtype = torch_dtype
        else:
            self.dtype = dtype

    def as_tensor(self, tensor: Tensor) -> Tensor:
        return torch.tensor(tensor, dtype=self.dtype)

    def get_zero_state(self, qnum: int) -> Tensor:
        state = torch.zeros(
            torch.pow(torch.tensor(2), torch.tensor(qnum)),
            dtype=self.dtype,
        )
        state[0] = 1
        return state

    def reshape(self, state: Tensor, shape: Sequence) -> Tensor:
        return torch.reshape(state, shape)

    def ravel(self, state: Tensor) -> Tensor:
        return torch.ravel(state)

    def stack(self, states: Sequence[Tensor], axis: int = 0) -> Tensor:
        return torch.stack(states, axis=axis)

    def real(self, state: Tensor) -> Tensor:
        return torch.real(state)

    def sum(self, state: Tensor, axis: int | None = None) -> Tensor:
        return torch.sum(state, axis=axis)

    def conj(self, state: Tensor) -> Tensor:
        return torch.conj(state)

    def sqrt(self, state: Tensor) -> Tensor:
        return torch.sqrt(state)

    def copy(self, state: Tensor) -> Tensor:
        return state.clone()

    def dot(self, state1: Tensor, state2: Tensor) -> Tensor:
        state1 = torch.as_tensor(state1)
        state2 = torch.as_tensor(state2).type_as(state1)
        return torch.dot(state1, state2)
