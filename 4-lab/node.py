import sys
from typing import Callable

from mpi4py import MPI


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

    def run(self, func: Callable, *args, **kwargs):
        start_func_time = MPI.Wtime()
        result = func(self, *args, **kwargs)
        self.set_state(runtime=MPI.Wtime() - start_func_time)
        self.set_state(result=result)

    def share_state_with_slaves(self, key):
        self.__state[key] = self.comm.bcast(self.state.get(key), root=self.root)
