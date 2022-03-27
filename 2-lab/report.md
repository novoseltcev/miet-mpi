# Контрольные вопросы

---

1. **Как происходит передача данных от одного процесса всем?**

> *Ответ:*
> MPI_Bcast, MPI_Scatter

2. **Как происходит передача данных от всех процессов одному?**

> *Ответ:*
> MPI_Gather, MPI_Reduce

3. **Какие используются в MPI для синхронизации вычислений?**

> *Ответ:*
> MPI_Barrier

4. **Как организуется неблокирующий обмен данными между процессами?**

> *Ответ:*
> К названию функций добавляется приставка I (MPI_Isend, MPI_Ibcast)

5. **Как организуется одновременное выполнение прием и передачи данных?**

> *Ответ:*
> MPI_Sendrecv

# Выполнение:

---

```text
➜  2-lab git:(2-lab) ✗ sh run.sh 4
Slave#2 | stopped | exec time=0.007462838
Slave#3 | stopped | exec time=0.007300948
Slave#1 | stopped | exec time=0.007301071
Master | interrupted | counter=3001 | exec time=0.007921428
➜  2-lab git:(2-lab) ✗ sh run.sh 8
Slave#6 | stopped | exec time=0.007147584
Slave#7 | stopped | exec time=0.00748977
Slave#5 | stopped | exec time=0.007626708
Slave#4 | stopped | exec time=0.00783351
Slave#3 | stopped | exec time=0.008353229
Slave#1 | stopped | exec time=0.007709971
Slave#2 | stopped | exec time=0.008812497
Master | interrupted | counter=7001 | exec time=0.021161317
```
