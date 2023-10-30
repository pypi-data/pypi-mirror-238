from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from typing import Any

import numpy as np

from ..gate import gates, max_qubit_num
from ..topo import adjacency_list, qubit_used

Tensor = Any


class StateVectorSimulatorError(Exception):
    """state vector simulation error"""


class StateVectorSimulator:
    def __init__(self, topo: bool = True):
        self.topo = topo

    def as_tensor(self, Tensor) -> Tensor:
        raise NotImplementedError

    def reshape(self, state: Tensor, shape: Sequence) -> Tensor:
        raise NotImplementedError

    def ravel(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def stack(self, states: Sequence[Tensor], axis: int = 0) -> Tensor:
        raise NotImplementedError

    def real(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def sum(self, state: Tensor, axis: int | None = None) -> Tensor:
        raise NotImplementedError

    def conj(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def sqrt(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def copy(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def dot(self, state1: Tensor, state2: Tensor) -> Tensor:
        raise NotImplementedError

    def get_zero_state(self, qnum: int) -> Tensor:
        raise NotImplementedError

    def reshape_single(
        self,
        state: Tensor,
        qnum: int,
        target: int,
    ) -> Tensor:
        shape = (1 << target, 2, 1 << (qnum - target - 1))
        return self.reshape(state, shape)

    def reshape_double(
        self,
        state: Tensor,
        qnum: int,
        target1: int,
        target2: int,
    ) -> Tensor:
        shape = (
            1 << target1,
            2,
            1 << (target2 - target1 - 1),
            2,
            1 << (qnum - target2 - 1),
        )
        return self.reshape(state, shape)

    def single_gate(
        self,
        state: Tensor,
        gate_name: str,
        qnum: int,
        target: int,
        *args,
    ) -> Tensor:
        state = self.reshape_single(state, qnum, target)

        if gate_name in gates:
            mat_func = gates[gate_name]["matrix"]
            if mat_func is None:
                return self.ravel(state)
            param = gates[gate_name]["param"]
            if param == 0:
                mat = mat_func()
            else:
                if len(args) != param:
                    raise StateVectorSimulatorError("Wrong number of parameters.")
                mat = mat_func(*args)
            state = self.as_tensor(mat) @ state[:,]
        else:
            raise StateVectorSimulatorError("non-existent quantum gate")
        return self.ravel(state)

    def multi_gate(
        self,
        state: Tensor,
        gate: str,
        qnum: int,
        ctrl: int,
        target: int,
    ) -> Tensor:
        """Support CX(CNOT), CY, CZ"""
        if ctrl < target:
            state = self.reshape_double(state, qnum, ctrl, target)
            if gate in ["CX", "CNOT"]:
                a, b = state[:, 1, :, 0, :], state[:, 1, :, 1, :]
                u = self.stack([b, a], axis=2)
                state = self.stack([state[:, 0, :, :, :], u], axis=1)
            elif gate == "CY":
                a, b = 1j * state[:, 1, :, 0, :], -1j * state[:, 1, :, 1, :]
                u = self.stack([b, a], axis=2)
                state = self.stack([state[:, 0, :, :, :], u], axis=1)
            elif gate == "CZ":
                a, b = state[:, 0, :, 1, :], -1 * state[:, 1, :, 1, :]
                u = self.stack([a, b], axis=1)
                state = self.stack([state[:, :, :, 0, :], u], axis=3)
            return self.ravel(state)
        else:
            state = self.reshape_double(state, qnum, target, ctrl)
            if gate in ["CX", "CNOT"]:
                a, b = state[:, 0, :, 1, :], state[:, 1, :, 1, :]
                u = self.stack([b, a], axis=1)
                state = self.stack([state[:, :, :, 0, :], u], axis=3)
            elif gate == "CY":
                a, b = 1j * state[:, 0, :, 1, :], -1j * state[:, 1, :, 1, :]
                u = self.stack([b, a], axis=1)
                state = self.stack([state[:, :, :, 0, :], u], axis=3)
            elif gate == "CZ":
                a, b = state[:, 0, :, 1, :], -1 * state[:, 1, :, 1, :]
                u = self.stack([a, b], axis=1)
                state = self.stack([state[:, :, :, 0, :], u], axis=3)
            return self.ravel(state)

    def swap(
        self,
        state: Tensor,
        qnum: int,
        q1: int,
        q2: int,
    ) -> Tensor:
        q1, q2 = min(q1, q2), max(q1, q2)
        state = self.reshape_double(state, qnum, q1, q2)
        a, b, c, d = (
            state[:, 0, :, 0, :],
            state[:, 0, :, 1, :],
            state[:, 1, :, 0, :],
            state[:, 1, :, 1, :],
        )
        u = self.stack([a, c], axis=2)
        v = self.stack([b, d], axis=2)
        state = self.stack([u, v], axis=1)
        return self.ravel(state)

    def measure(
        self,
        state: Tensor,
        qnum: int,
        target: int,
    ) -> tuple[int, Tensor]:
        state = self.reshape_single(state, qnum, target)
        p0 = self.real(self.sum(state[:, 0, :] * self.conj(state[:, 0, :])))
        res = 0
        if np.random.uniform() < p0:
            state[:, 1, :] = 0
            state /= self.sqrt(p0)
        else:
            p1 = 1 - p0
            state[:, 0, :] = 0
            state /= self.sqrt(p1)
            res = 1
        state = self.ravel(state)
        return res, state

    def shift(
        self,
        state: Tensor,
        qnum: int,
        mq: Sequence[int],
    ) -> Tensor:
        qidx = {}
        idxq = {}
        for i in range(qnum):
            qidx[i] = i
            idxq[i] = i

        for i, m in enumerate(mq):
            if qidx[m] == i:
                continue
            state = self.swap(state, qnum, i, qidx[m])
            q = idxq[i]
            qidx[q] = qidx[m]
            qidx[m] = i
            idxq[i] = m
            idxq[qidx[q]] = q
        return state

    def check(self, line_data: Iterable) -> tuple[int, dict]:
        qdic = {}
        qnum = 0
        for idx, line in enumerate(line_data):
            line = line.strip()
            if not line:
                continue
            strArr = line.split(" ")
            if strArr[0] not in gates and strArr[0] not in ["CNOT", "CX", "CY", "CZ"]:
                raise StateVectorSimulatorError(
                    f"simulate error: in line {idx}, gate error of {strArr[0]}"
                )
            # if len(strArr) < 2 or len(strArr) > 4:
            if len(strArr) < 2:
                raise StateVectorSimulatorError(
                    f"simulate error: in line {idx}, qbit number error"
                )

            if strArr[1][0] != "Q" or not strArr[1][1:].isdigit():
                raise StateVectorSimulatorError(
                    f"simulate error: in line {idx}, qbit syntax error"
                )

            if self.topo:
                if not int(strArr[1][1:]) in qubit_used:
                    raise StateVectorSimulatorError(
                        f"simulate error: in line {idx}, invalid qubit"
                    )

            if strArr[1] not in qdic:
                qdic[strArr[1]] = qnum
                qnum += 1

            if strArr[0] in ["CZ", "CY", "CX", "CNOT"]:
                if len(strArr) != 3:
                    raise StateVectorSimulatorError(
                        f"simulate error: in line {idx}, qbit number error"
                    )

                if strArr[2][0] != "Q" or not strArr[2][1:].isdigit():
                    raise StateVectorSimulatorError(
                        f"simulate error: in line {idx}, qbit syntax error"
                    )

                if self.topo:
                    if not int(strArr[2][1:]) in qubit_used:
                        raise StateVectorSimulatorError(
                            f"simulate error: in line {idx}, invalid qubit"
                        )

                    if (
                        sorted([int(strArr[1][1:]), int(strArr[2][1:])])
                        not in adjacency_list
                    ):
                        raise StateVectorSimulatorError(
                            f"simulate error: in line {idx}, invalid mapping"
                        )

                if strArr[2] not in qdic:
                    qdic[strArr[2]] = qnum
                    qnum += 1

            if strArr[0] in gates and gates[strArr[0]]["matrix"] is not None:
                if len(strArr) != (gates[strArr[0]]["param"] + 2):
                    raise StateVectorSimulatorError(
                        f"simulate error: in line {idx}, qbit number error"
                    )

        if qnum > max_qubit_num:
            raise StateVectorSimulatorError(
                f"simulate error: qbit number `{qnum}` is too large, "
                "can not simulate."
            )

        return qnum, qdic

    def getstate(
        self,
        line_data: Iterable,
        qnum: int,
        qdic: dict,
        **kwargs,
    ) -> tuple[Tensor, list]:
        state = self.get_zero_state(qnum)
        mq = []
        for line in line_data:
            line = line.strip()
            if not line:
                continue
            strArr = line.split(" ")
            qid1 = qdic[strArr[1]]
            if strArr[0] == "M":
                mq.append(qid1)
            else:
                if strArr[0] in ["CZ", "CY", "CX", "CNOT"]:
                    qid2 = qdic[strArr[2]]
                    state = self.multi_gate(state, strArr[0], qnum, qid1, qid2)
                else:
                    if gates[strArr[0]]["matrix"] is None:
                        continue
                    theta = []
                    for v in strArr[2:]:
                        theta.append(eval(v, kwargs))
                    state = self.single_gate(state, strArr[0], qnum, qid1, *theta)
        return state, mq

    def sample(
        self,
        qcis: str,
        shots: int = 100,
        dict_format: bool = True,
        **kwargs,
    ) -> dict[str, int]:
        line_data = qcis.split("\n")
        qnum, qdic = self.check(line_data)
        state, mq = self.getstate(line_data, qnum, qdic, **kwargs)
        state = self.shift(state, qnum, mq)
        state = self.conj(state) * state
        mq_len = len(mq)
        state = self.reshape(state, [1 << mq_len, 1 << (qnum - mq_len)])
        p = self.real(self.sum(state, axis=1))
        p_norm = p / sum(p)
        r = np.random.choice(1 << mq_len, shots, p=p_norm)
        if dict_format:
            return {bin(k)[2:].zfill(mq_len): v for k, v in Counter(r).items()}
        else:
            answer = [bin(v)[2:].zfill(mq_len) for v in r]
            return "".join(answer)
        # qdic_rev = {v: int(k[1:]) for k, v in qdic.items()}
        # answer.append([qdic_rev[i] for i in mq])

    def probs(
        self,
        data: str,
        **kwargs,
    ) -> Tensor:
        line_data = data.split("\n")
        qnum, qdic = self.check(line_data)
        state, mq = self.getstate(line_data, qnum, qdic, **kwargs)
        state = self.shift(state, qnum, mq)
        state = self.conj(state) * state
        mq_len = len(mq)
        state = self.reshape(state, [1 << mq_len, 1 << (qnum - mq_len)])
        return self.real(self.sum(state, axis=1))

    def state(
        self,
        data: str,
        **kwargs,
    ) -> Tensor:
        line_data = data.split("\n")
        qnum, qdic = self.check(line_data)
        state, _ = self.getstate(line_data, qnum, qdic, **kwargs)
        return state
