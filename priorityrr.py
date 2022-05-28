import heapq
from collections import deque

from scheduler import Scheduler
from utils import Schedule
from process import Process


class PriorityRR(Scheduler):

    def __init__(self, process_list: list[Process], time_quantum: int):
        """
        attributes

        self.pq : pq is a priority queue, saving (priority, last time the process came out from cpu, pid)
                  first two values are used to sort and decide which process to use

        self.process_list : sorted ascending order by arrival_time for convenience

        self.process_dict : it'll store process, key : pid, value : Process
        """
        super().__init__(process_list)
        self.time_quantum = time_quantum
        self.pq = []
        self.process_list = deque(sorted(process_list, key=lambda x: x.arrival_time))
        self.process_dict = {}
        for p in process_list:
            self.process_dict[p.process_ID] = p

    def do_schedule(self) -> Schedule:
        """
        last_out_process is pointer variable which stores the last process used CPU
        """
        last_out_process = None

        while True:
            if self.process_list:
                # put process that arrived since the last process used cpu until current time into ready queue(self.pq)
                if self.process_list[0].arrival_time <= self.current_time:
                    while self.process_list and self.process_list[0].arrival_time <= self.current_time:
                        p = self.process_list.popleft()
                        heapq.heappush(self.pq, (p.priority, p.last_time_out, p.process_ID))
                # No process to use cpu in current time, proceed time to the arrival time of the next process
                if not last_out_process and not self.pq:
                    self.current_time = self.process_list[0].arrival_time
                    self.schedule.add_schedule("None", self.current_time)
                    continue
            # all process is complete
            elif not last_out_process and not self.pq:
                break
            # put the incomplete back to the ready queue
            if last_out_process:
                # slight tie breaker needed, add small number to make sure it's behind the process who went in right now
                heapq.heappush(self.pq, (last_out_process.priority, last_out_process.last_time_out + 0.001, last_out_process.process_ID))

            # pop from the pq, that's the process that should use cpu right now
            pid = heapq.heappop(self.pq)[2]
            last_out_process = self.process_dict[pid]
            use_time = self.time_quantum if self.time_quantum <= last_out_process.time_left else last_out_process.time_left
            last_out_process.use_cpu(use_time, self.current_time)
            self.current_time += use_time
            self.schedule.add_schedule(last_out_process.process_ID, self.current_time)
            if last_out_process.process_complete:
                last_out_process = None

        return self.schedule
