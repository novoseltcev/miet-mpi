from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
begin_time = MPI.Wtime()
if rank == 0:
    counter = 0
    while True:
        value, source_rank = comm.recv()
        counter += 1
        if value == -1:
            print(f'Master handled {counter} messages '
                  f'and terminated from slave-{source_rank} '
                  f'with exec time: {MPI.Wtime() - begin_time}')
            exit(0)
else:
    for value in range(1000, -2, -1):
        comm.send((value, rank), dest=0)
    print(f'Slave-{rank} stopped with exec time: {MPI.Wtime() - begin_time}')
