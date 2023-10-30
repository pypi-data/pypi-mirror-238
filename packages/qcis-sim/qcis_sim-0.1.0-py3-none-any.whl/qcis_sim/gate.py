import numpy as np

max_qubit_num = 16

gates = {
    "I": {
        "matrix": None,
    },
    "B": {
        "matrix": None,
    },
    "M": {
        "matrix": None,
    },
    "H": {
        "matrix": lambda: 1
        / np.sqrt(2)
        * np.array(
            [
                [1.0, 1.0],
                [1.0, -1.0],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "X": {
        "matrix": lambda: np.array(
            [
                [0.0, 1.0],
                [1.0, 0.0],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "Y": {
        "matrix": lambda: np.array(
            [
                [0.0, -1j],
                [1j, 0.0],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "Z": {
        "matrix": lambda: np.array(
            [
                [1.0, 0.0],
                [0.0, -1.0],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "S": {
        "matrix": lambda: np.array(
            [
                [1.0, 0.0],
                [0.0, 1j],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "T": {
        "matrix": lambda: np.array(
            [
                [1.0, 0.0],
                [0.0, np.exp(np.pi / 4.0 * 1j)],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "SD": {
        "matrix": lambda: np.array(
            [
                [1.0, 0.0],
                [0.0, -1j],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "TD": {
        "matrix": lambda: np.array(
            [
                [1.0, 0.0],
                [0.0, np.exp(np.pi / 4.0 * -1j)],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "X2M": {
        "matrix": lambda: 1
        / np.sqrt(2)
        * np.array(
            [
                [1.0, 1j],
                [1j, 1.0],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "X2P": {
        "matrix": lambda: 1
        / np.sqrt(2)
        * np.array(
            [
                [1.0, -1j],
                [-1j, 1.0],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "Y2M": {
        "matrix": lambda: 1
        / np.sqrt(2)
        * np.array(
            [
                [1.0, 1.0],
                [-1.0, 1.0],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "Y2P": {
        "matrix": lambda: 1
        / np.sqrt(2)
        * np.array(
            [
                [1.0, -1.0],
                [1.0, 1.0],
            ],
            dtype=complex,
        ),
        "param": 0,
    },
    "RX": {
        "matrix": lambda theta: np.array(
            [
                [np.cos(theta / 2), -1j * np.sin(theta / 2)],
                [-1j * np.sin(theta / 2), np.cos(theta / 2)],
            ],
            dtype=complex,
        ),
        "param": 1,
    },
    "RY": {
        "matrix": lambda theta: np.array(
            [
                [np.cos(theta / 2), -1 * np.sin(theta / 2)],
                [np.sin(theta / 2), np.cos(theta / 2)],
            ],
            dtype=complex,
        ),
        "param": 1,
    },
    "RZ": {
        "matrix": lambda theta: np.array(
            [
                [np.exp(-1j * theta / 2), 0],
                [0, np.exp(1j * theta / 2)],
            ],
            dtype=complex,
        ),
        "param": 1,
    },
    "RXY": {
        "matrix": lambda theta, phi: np.array(
            [
                [np.cos(theta / 2), -1j * np.exp(-1j * phi / 2) * np.sin(theta / 2)],
                [-1j * np.exp(1j * phi / 2) * np.sin(theta / 2), np.cos(theta / 2)],
            ],
            dtype=complex,
        ),
        "param": 2,
    },
}
