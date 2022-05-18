def pri(n: int, burst_time: list, priority: list):
    process_list = list(range(1,n+1))
    turn_around_time = []
    waiting_time = []

    # sort
    for i in range(0, len(priority) - 1):
        for j in range(0, len(priority) - i - 1):
            if priority[j] > priority[j + 1]:
                swap = priority[j]
                priority[j] = priority[j + 1]
                priority[j + 1] = swap

                swap = burst_time[j]
                burst_time[j] = burst_time[j + 1]
                burst_time[j + 1] = swap

                swap = process_list[j]
                process_list[j] = process_list[j + 1]
                process_list[j + 1] = swap

    waiting_time.insert(0, 0)
    turn_around_time.insert(0, burst_time[0])

    # Calculating of waiting time and Turn Around Time of each process
    for i in range(1, len(process_list)):
        waiting_time.insert(i, waiting_time[i - 1] + burst_time[i - 1])
        turn_around_time.insert(i, waiting_time[i] + burst_time[i])

    # calculating average waiting time and average turn around time
    avg_turn_around_time = 0
    avg_waiting_time = 0
    for i in range(0, len(process_list)):
        avg_waiting_time = avg_waiting_time + waiting_time[i]
        avg_turn_around_time = avg_turn_around_time + turn_around_time[i]
    avg_waiting_time = float(avg_waiting_time) / n
    avg_turn_around_time = float(avg_turn_around_time) / n

    response = dict(data=[], avg_tat=avg_turn_around_time, avg_wait_time=avg_waiting_time)


    for i in range(0, n):
        response['data'].append(dict(
            pid=process_list[i], burst_time=burst_time[i], turn_around_time=turn_around_time[i],
            waiting_time=waiting_time[i], pri=priority[i]))

    return response