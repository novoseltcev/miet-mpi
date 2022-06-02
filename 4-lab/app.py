from functools import reduce, wraps

import numpy as np
from mpi4py import MPI

from node import MPINode


def read_task_queue(node: MPINode):
    queue = []
    with open('tasks.txt', 'r') as fd:
        while line := fd.readline():
            queue.append(np.array(tuple(map(int, line.split())), dtype='int64'))

    poly_size = reduce(lambda x, y: x + y - 1, map(lambda poly: poly.size, queue))
    queue = list(map(lambda poly: np.pad(poly, (0, poly_size - poly.size)), queue))
    node.set_state(
        queue=queue,
        poly_size=poly_size
    )


def define_poly(length: int) -> MPI.Datatype:
    PolynomType = MPI.SINT64_T.Create_contiguous(count=length)
    PolynomType.Set_name('polynom')
    PolynomType.Commit()
    return PolynomType


def poly_mul(p_first: list, p_second: list):
    n_first = len(p_first)
    n_second = len(p_second)
    n_result = n_second + n_first - 1
    result = [0] * n_result
    for k in range(n_result):
        for i in range(k + 1):
            j = k - i
            if (j < n_second) and (i < n_first):
                result[k] += p_first[i] * p_second[j]
    return result


def np2list2np(func):
    @wraps(func)
    def wrapper(array: np.ndarray, *args, **kwargs):
        array = list(map(list, array))
        return np.array(
            func(array, *args, **kwargs), dtype='int64'
        )

    return wrapper


@np2list2np
def mul_polys(array: list, max_size: int):
    return reduce(poly_mul, array)[:max_size]


def distribute_tasks(node: MPINode):
    queue = node.state['queue']
    size = node.comm.Get_size()
    result = []
    poly_per_task = len(queue) // size

    for _ in range(size):
        task, queue = queue[:poly_per_task], queue[poly_per_task:]
        result.append(task)
    result[0] += queue
    node.set_state(tasks=result)


def main(node: MPINode):
    task = node.comm.scatter(node.state.get('tasks'), root=node.root)
    poly_size = node.state['poly_size']
    parallel_result = mul_polys(task, poly_size)
    recv_result = node.comm.gather(parallel_result, root=node.root)
    if node.is_master:
        return mul_polys(recv_result, poly_size)


if __name__ == '__main__':
    node = MPINode(comm=MPI.COMM_WORLD, root=0)

    if node.is_master:
        read_task_queue(node)
    node.share_state_with_slaves('poly_size')
    node.set_state(poly_type=node.define_type([np.int32] * node.state['poly_size'], 2))

    if node.is_master:
        distribute_tasks(node)

    start_func_time = MPI.Wtime()
    node.set_state(result=main(node))
    node.set_state(runtime=MPI.Wtime() - start_func_time)

    print(f'Proc#{node.comm.Get_rank()} | {node.runtime=}')
    node.stop_slave()
    print(f'{node.exec_time=}')
    print(f'{node.result=}')
