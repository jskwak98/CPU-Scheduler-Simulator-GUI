"""
FCFS Scheduler
example pseudo code

hope it helps how Process class works and Scheduler do its work

note that what scheduler do is only
1. decide which process should use CPU in current time
2. keep track of current time
3. then add the information (pid, last_time_out) to schedule

you do not need to worry about WT, RT, TT
it's all computed within Process class only if you use_cpu(burst_time, current_time)
"""
from scheduler import Scheduler
from utils import Schedule
from process import Process

class FCFS(Scheduler):

    def __init__(self, process_list: list[Process]):
        super().__init__(process_list)

    def do_schedule(self) -> Schedule:
        # sort and decide which process to be popped and use cpu
        # sort process list by process.arrival_time
        # for process in process_list:
        # process.use_cpu(process.cpu_burst_time, self.current_time)
        # self.current_time += process.cpu_burst_time
        # self.schedule.add_schedule(process.process_ID, self.current_time)
        return self.schedule
