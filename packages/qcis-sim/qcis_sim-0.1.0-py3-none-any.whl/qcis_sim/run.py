from __future__ import annotations

from .backend import NumpyBackend, TorchBackend
from .backend.state_vector_simulator import StateVectorSimulator
from .topo import config


def run(
    qcis: str,
    shots: int = 100,
    backend: str = "numpy",
    topo: bool = True,
    dict_format: bool = True,
) -> str | dict[str, int]:
    backend = backend.lower()
    if backend == "numpy":
        bk = NumpyBackend(topo=topo)
    elif backend in ["pytorch", "torch"]:
        bk = TorchBackend(topo=topo)
    else:
        raise TypeError("Invalid backend.")

    return bk.sample(qcis=qcis, shots=shots, dict_format=dict_format)


def get_info() -> dict:
    return config
