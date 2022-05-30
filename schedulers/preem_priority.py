from process import Process
from utils import Schedule

class PPriority:
    def __init__(self, process_list: list):
        self.process_list = process_list

    def do_schedule(self):
        # 레디큐.
        ready_q = []

        # 프로세스 a 를 레디큐에 넣는 함수
        def to_ready(a: Process):
            if ready_q:   #큐에 뭐 들어 있으면
                for i in range(0, len(ready_q)):
                    if a.priority < ready_q[i].priority:   #새로 큐에 들어온게 더 우선순위 높으면
                        ready_q[i:i] = [a]   #그 앞에 넣음
                        break
                    elif i == len(ready_q) - 1:   #큐에 있는 것들보다 우선순위 제일 뒤면
                        ready_q.append(a)   #맨 뒤에 넣음
            else:
                ready_q.append(a)
            return 0

        # 프로세스 리스트 초반 세팅. 도착시간 빠르고 우선순위 높은 거 먼저오게 정렬
        p_l = []
        p_l.append(self.process_list[0])
        for i in range(1, len(self.process_list)):
            for j in range(0, len(p_l)):
                if self.process_list[i].arrival_time < p_l[j].arrival_time:  # 도착시간이 더 빠르면 그 앞에 넣기
                    p_l[j:j] = [self.process_list[i]]
                    break
                elif self.process_list[i].arrival_time == p_l[j].arrival_time:  # 도착시간 같을 때
                    if self.process_list[i].priority < p_l[j].priority:  # 우선순위 높으면 그 앞에 놓기
                        p_l[j:j] = [self.process_list[i]]
                        break
                if j == len(p_l) - 1:  # p_l 중 젤 늦게 도착하면서 우선순위도 젤 늦으면
                    p_l.append(self.process_list[i])

        # R = 실행중인 프로세스, p_l = 아직 레디큐에도 안 들어간 프로세스들
        R = p_l[0]
        p_l = p_l[1:]

        #처음 실행되는건 응답시간 무조건 0
        R.response_time = 0

        # t = 시각
        t = R.arrival_time

        # 간테 차트를 위한 리스트. [p1,10] 이면 10까지 p1이 run 했다는 뜻.
        gan = []
        if t > 0:
            gan.append(['None', t])

        # 무한루프 시작
        while True:
            if p_l:  # 도착 안 한 프로세스가 있을 때
                BBB = p_l[0].arrival_time

                if (t + R.time_left) < BBB:  # 실행 끝날 때까지 새 프로세스 도착 안하면
                    t = t + R.time_left  # 실행중인 프로세스 종료 시간으로 바꿔주고
                    for proc in ready_q:  # 대기시간 증가
                        proc.wait_time = proc.wait_time + R.time_left
                    gan.append([R.process_ID, t])  # 간테차트에 그리고
                    R.time_left = 0  # 실행중인거 다 수행
                    R.turnaround_time = t - R.arrival_time  # 반환시간 기록

                    if ready_q:   #레디큐에 있으면
                        R = ready_q[0]  # 레디큐 맨 앞에 있는 걸 실행
                        ready_q = ready_q[1:]  # 레디큐에서 뺐으니 삭제해줌

                        if R.response_time == -1:  # 큐에 있던 놈이 실행되는 거면
                            R.response_time = R.wait_time  # 응답시간 = 대기시간
                    else :   #레디큐에 없으면
                        t = BBB   #그 다음 오는 놈인 p_l[0] 이 실행되니
                        R = p_l[0]
                        p_l = p_l[1:]
                        gan.append(['None', t])  # 간테차트. 이땐 아무것도 없음

                        R.response_time = 0  # 도착하고 바로 실행되니 응답시간 0

                    continue

                elif (t + R.time_left) > BBB:  # 실행 중에 도착하면
                    for proc in ready_q:  # 대기시간 증가
                        proc.wait_time = proc.wait_time + BBB - t
                    R.time_left = R.time_left - BBB + t  # 실행중인거 남은 시간 수정
                    t = BBB  # 시간을 바꿔주고

                    if R.priority <= p_l[0].priority:  # 실행 중인게 더 우선순위 높거나 같으면
                        to_ready(p_l[0])  # 도착한거 큐에 넣음
                        p_l = p_l[1:]
                        continue
                    else:  # 도착한게 더 우선순위 높으면
                        to_ready(R)  # 실행 중이던거 큐에 넣음
                        gan.append([R.process_ID, t])  # 간태차트
                        R = p_l[0]  # 도착한거 실행
                        p_l = p_l[1:]

                        R.response_time = 0   #도착하고 바로 실행되니 응답시간 0
                        continue
                else:  # 실행 끝 = 도착시간
                    for proc in ready_q:  # 대기시간 증가
                        proc.wait_time = proc.wait_time + BBB - t
                    R.time_left = 0  # 실행중인거 다 수행
                    t = BBB  # 시간을 바꿔주고

                    R.turnaround_time = t - R.arrival_time  # 반환시간 기록
                    gan.append([R.process_ID, t])  # 간태차트
                    to_ready(p_l[0])  # 도착한거 큐에 넣음
                    p_l = p_l[1:]
                    R = ready_q[0]  # 큐 제일 앞에거 실행
                    ready_q = ready_q[1:]

                    if (R.response_time == -1) and (R.wait_time == 0):   #도착한놈이 바로 실행되면
                        R.response_time = 0  # 도착하고 바로 실행되니 응답시간 0
                    elif R.response_time == -1 : #큐에 있던 놈이 처음 실행되는 거면
                        R.response_time = R.wait_time   #응답시간 = 대기시간

                    continue
            else:  # 도착 안한게 없을 때
                if ready_q:  # 레디큐에 프로세스가 남아있을 때
                    t = t + R.time_left  # 시간을 바꿔주고
                    for proc in ready_q:  # 대기시간 증가
                        proc.wait_time = proc.wait_time + R.time_left
                    R.time_left = 0  # 실행중인거 다 수행
                    R.turnaround_time = t - R.arrival_time  # 반환시간 기록
                    gan.append([R.process_ID, t])  # 간태차트
                    R = ready_q[0]  # 큐 제일 앞에거 실행
                    ready_q = ready_q[1:]

                    if R.response_time == -1 : #아직 한번도 실행 안됐던 거면
                        R.response_time = R.wait_time   #응답시간 = 대기시간

                    continue
                else:  # 레디큐에 프로세스가 없을 때
                    if R:  # 실행중인게 있을 때
                        t = t + R.time_left  # 시간을 바꿔주고
                        R.time_left = 0  # 실행중인거 다 수행
                        R.turnaround_time = t - R.arrival_time  # 반환시간 기록
                        gan.append([R.process_ID, t])  # 간태차트
                        break
                    else:  # 실행 중인것도 없을 때?
                        break

        # 평균 대기시간 구하기
        total_wait = 0
        for proc in self.process_list:
            total_wait += proc.wait_time
        ave_wait = total_wait / len(self.process_list)

        # 평균 응답시간 구하기
        total_response = 0
        for proc in self.process_list:
            total_response += proc.response_time
        ave_response = total_response / len(self.process_list)

        # 평균 반환시간 구하기
        total_turn = 0
        for proc in self.process_list:
            total_turn += proc.turnaround_time
        ave_turn = total_turn / len(self.process_list)

        # 결과값 : 프로세스 리스트, 평균 대기시간, 평균 응답시간, 평균 반환시간, 간테차트용 리스트
        return_schedule = Schedule()
        return_schedule.schedule = gan
        return return_schedule
