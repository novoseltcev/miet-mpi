# Контрольные вопросы

---

1. **В чем состоят основы технологии MPI?**

> *Ответ:*
> Обмен сообщениями между процессами в кластере

2. **На чем состоят основные преимущества и недостатки технологии MPI?**

> *Ответ:*
>
> `+` простота аппаратуры
>
> `+` акцент внимания на процессе обмена сообщениями, а не низкоуровнего доступа к общей памяти
>
> `+` единый интерфейс стандартом MPI
> 
> `-` latency передачи сообщений: инициализация отправки и передача через топологии
>
> `-` cложность программирования и отладки 

3. **Что понимается под параллельной программой в рамках технологии MPI?**

> *Ответ:*
> Несколько процессов, которые общаются с друг другом посредством сообщений

4. **Как происходит инициализация и завершение MPI программ?**

> *Ответ:*
>
> MPI_Init(&argc, &argv);
> 
> MPI_Finalize();

5. **Как происходит передача и прием сообщений MPI программе?**

> *Ответ:*
> 
> Коммуникатор объединяет процессы в группы
>  
> Инта-коммуникаторы передают сообщения внутри групп, а интер - между группами
> 
> Общение производится с помощью операций отправки и приёма сообщений, которые бывают двух типов: 
> + point-to-point 
> + коллективные


# Выполнение:
```text
➜  1-lab git:(1-lab) ✗ sh run.sh 4
Slave#1 stopped (exec: 0.002401894)
Slave#2 stopped (exec: 0.003447657)
Slave#3 stopped (exec: 0.003781841)
Master handled 1914 messages and terminated from Slave#1 (exec : 0.004337455)
➜  1-lab git:(1-lab) ✗ sh run.sh 8
Slave#5 stopped (exec: 0.004100501)
Slave#4 stopped (exec: 0.003983008)
Slave#6 stopped (exec: 0.004220908)
Slave#1 stopped (exec: 0.004286093)
Slave#2 stopped (exec: 0.004295918)
Slave#7 stopped (exec: 0.004307119)
Master handled 4920 messages and terminated from Slave#6 (exec : 0.011401314)
Slave#3 stopped (exec: 0.002512518)
```
---