"""
FCFS Scheduler

이 의사 코드가 어떻게 프로세스 클래스가 작동하고, 
스케쥴러가 이를 처리할지에 대해 도움이 되길 바랍니다.

스케쥴러는 다음 아래의 것만 수행한다는 것을 유념하십시오.

1. 어떤 프로세스가 현재 CPU를 사용하게 될지 결정하기
2. 현재 시간을 추적하기
3. 프로세스 ID, last_time_out과 같은 정보들을 스케쥴에 추가하기
(WT, RT, TT와 같은 것에 대해 걱정할 필요는 없습니다. 
use_cpu(burst_time, current_time)를 사용하는 경우에만 프로세스 클래스 내에서 모두 계산됩니다.)
"""

from asyncore import poll3
from collections import deque
from sys import ps1
from scheduler import Scheduler
from utils import Schedule
from process import Process

class FCFS(Scheduler):

#process_ID(str)         : name of the process; P1 P2 etc...; must be denoted at the Gantt Chart
#arrival_time(int)       : arrival time of the process; larger than 0
#cpu_burst_time(int)     : required cpu burst time of process; larger than 0

    def __init__(self, process_list: list[Process]):
        super().__init__(process_list)
        self.process_list = deque(sorted(process_list, key=lambda x: x.arrival_time))

    def do_schedule(self) -> Schedule:
        self.schedule = Schedule()
        while True:
            # 남은 process가 있고, 도착시간이 현재 시간보다 작거나 같으면
            if self.process_list and self.process_list[0].arrival_time <= self.current_time:
                # 가장 도착시간이 빠른 프로세스 Pop
                process = self.process_list.popleft()
                # 남은 시간만큼, 지금 시점에 cpu 사용
                process.use_cpu(process.time_left, self.current_time)
                # 사용 후 현재 시간 계산
                self.time += process.cpu_burst_time
                # 스케쥴에 결과를 기록하기
                self.schedule.add_schedule(process.process_ID, self.current_time)

            # 아직 process_list의 가장 빠른 process의 도착시간이 안돼서 CPU가 노는 경우
            elif self.process_list and self.process_list[0].arrival_time > self.current_time:
                self.schedule.add_schedule('None', self.current_time)
                self.current_time = self.process_list[0].arrival_time
                # 시간을 다음 도착할 process의 arrival time으로 바꿔줄것
                # 스케쥴에는 다음과 같이 기록해볼 것.
            # 끝난 경우
            else:
                return self.schedule

        # sort and decide which process to be popped and use cpu
        # sort process list by process.arrival_time
        # for process in process_list:
        # process.use_cpu(process.cpu_burst_time, self.current_time)
        # self.current_time += process.cpu_burst_time

        # self.schedule.add_schedule(process.process_ID, self.current_time)