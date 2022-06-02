import sys

from mpi4py import MPI
import numpy as np


class MPINode:
    def __init__(self, comm: MPI, root: int = 0) -> None:
        self._start_time = MPI.Wtime()
        self.__comm: MPI.Comm = comm
        self._root: int = root
        self.__state = {}

    @property
    def root(self) -> int:
        return self._root

    @property
    def comm(self) -> MPI.Comm:
        return self.__comm

    @property
    def state(self) -> dict:
        return self.__state

    @property
    def is_master(self) -> bool:
        return self.comm.Get_rank() == self.root

    @property
    def is_slave(self) -> bool:
        return not self.is_master

    @property
    def exec_time(self) -> float:
        return MPI.Wtime() - self._start_time

    @property
    def result(self) -> dict:
        return self.state.get('result')

    @property
    def runtime(self) -> dict:
        return self.state.get('runtime')

    def set_state(self, **kwargs) -> None:
        self.__state.update(**kwargs)

    def set_result(self, value) -> None:
        self.set_state(result=value)

    def stop_slave(self, code: int = 0):
        if self.is_slave:
            sys.exit(code)

    def share_state_with_slaves(self, key):
        self.__state[key] = self.comm.bcast(self.state.get(key), root=self.root)

    @staticmethod
    def define_type(types: list, count: int):
        mpi_types = {np.int32: MPI.INT, np.float64: MPI.DOUBLE}

        names = [str(i) for i in range(len(types))]
        dtypes = list(zip(names, types))
        buffer = np.zeros(count, dtype=dtypes)

        offsets = [buffer.dtype.fields[name][1] for name in names]

        result = MPI.Datatype.Create_struct([1] * len(types), offsets, [mpi_types[dtype] for dtype in types])
        result.Commit()
        return result
