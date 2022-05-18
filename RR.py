# process number, burst time, arrival time, time quantum을 순서대로 input으로 받는다.
def rr(n: int, arrival: list, burst_time: list, priority: list, tq: int):
    #burst_time의 원소들 int형으로 변환
    # for i in range(len(burst_time)):
    #     burst_time[i] = int(burst_time[i])
    # for i in range(len(arrival)):
    #     arrival[i] = int(arrival[i])
    turn_around_time = [0 for _ in range(len(burst_time))]
    burst_copy = list(burst_time)  # burst_time 리스트 복사
    burst_max = 0
    max_Q = 0
    min_arrival = min(arrival)
    for i in burst_time:
        burst_max += i
    process_list = [[0 for _ in range(burst_max + min_arrival + arrival[-1])] for _ in range(n)] #프로세스 목록
    time = [-1 for _ in range(len(process_list))]
    i = 0
    num = [-1,-1,-1,-1]
    q = []
    while True:
        for j in range(len(arrival)):
            if arrival[j] == i:
                q.append(j)
        for j in range(len(process_list)):
            if process_list[j][i] == 0 and time[j] < 0:

                if i != 0 and burst_copy[num[j]] != 0 and num[j] != -1:  # burst_copy의 길이가 0이 아니고 0초가 아니면
                    q.append(num[j])  # Burst_copy의 값이 남아있으므로 다시 queue에 넣음
                if q:
                    num[j] = q.pop(0)
                    if tq > burst_copy[num[j]]:  # time quantum의 길이가 burst_copy보다 길면
                        max_Q = burst_copy[num[j]]  # Burst_copy를 사용하고
                        burst_copy[num[j]] = 0  # 0으로 초기화
                    else:
                        max_Q = tq  # 그 반대면 time quantum의 길이를 사용하고
                        burst_copy[num[j]] -= tq  # burst_copy의 길이에서 time quantum의 길이만큼 뺌
                    for k in range(max_Q):
                        process_list[j][i + k] = num[j] + 1
                        turn_around_time[num[j]] = i + k + 1
                    time[j] = max_Q - 1
            if i != 0: #순서변경?
                for j in range(len(process_list)):
                    for k in range(j+1,len(process_list)):
                        getnum1 = 0
                        getnum2 = 0

                        if process_list[j][i-1] == process_list[k][i] and process_list[j][i-1] != 0:
                            change3 = process_list[j][i]
                            change4 = process_list[k][i]
                            while True:
                                if process_list[j][i+getnum1] != 0:
                                    process_list[j][i+getnum1] = 0
                                    getnum1 += 1
                                else :
                                    break
                            while True:
                                if process_list[k][i+getnum2] != 0:
                                    process_list[k][i+getnum2] = 0
                                    getnum2 += 1
                                else :
                                    break
                            for l in range(getnum1):
                                process_list[k][i+l] = change3
                            for l in range(getnum2):
                                process_list[j][i+l] = change4
        count = 0
        for j in process_list:
            for k in j:
                if k != 0:
                    count += 1
        for j in range(len(time)):
            time[j] -= 1
        i += 1
        if count == burst_max:
            break




    for l in range(len(turn_around_time)):
        turn_around_time[l] -= arrival[l]
    waiting_time = [0 for _ in range(len(burst_time))]
    for l in range(len(turn_around_time)):
        waiting_time[l] = turn_around_time[l] - burst_time[l]
    # return process_list, waiting_time, turn_around_time

    result = dict(data=[], avg_tat=sum(turn_around_time)/len(turn_around_time), avg_wait_time=sum(waiting_time)/len(waiting_time))

    for i in range(0, n):
        result['data'].append(dict(
            pid=process_list[i], burst_time=burst_time[i], turn_around_time=turn_around_time[i],
            waiting_time=waiting_time[i]))

    return result