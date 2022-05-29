from collections import deque
from scheduler import Scheduler
from utils import Schedule
from process import Process
import heapq


class SRTF(Scheduler):

    def __init__(self, process_list: list[Process]):
        super().__init__(process_list)
        self.pq = []
        self.process_list = deque(sorted(process_list, key=lambda x: x.arrival_time))
        self.process_dict = {}
        for p in process_list:
            self.process_dict[p.process_ID] = p

    def do_schedule(self) -> Schedule:
        # pointer variable
        last_out_process = None
        while True:
            if self.process_list:
                while self.process_list and self.process_list[0].arrival_time <= self.current_time:
                    p = self.process_list.popleft()
                    heapq.heappush(self.pq, (p.cpu_burst_time, p.process_ID))
                if not last_out_process and not self.pq:
                    self.current_time = self.process_list[0].arrival_time
                    self.schedule.add_schedule("None", self.current_time)
                    continue
            elif not last_out_process and not self.pq:
                break
            if last_out_process:
                heapq.heappush(self.pq, (last_out_process.cpu_burst_time, last_out_process.process_ID))

            pid = heapq.heappop(self.pq)[1]
            last_out_process = self.process_dict[pid]
            last_out_process.use_cpu(1, self.current_time)
            self.current_time += 1
            self.schedule.add_schedule(pid, self.current_time)
            if last_out_process.process_complete:
                last_out_process = None

        return self.schedule
