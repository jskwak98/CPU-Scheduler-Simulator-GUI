"""
FCFS Scheduler
example
"""
from scheduler import Scheduler
from utils import Schedule
from process import Process

class FCFS(Scheduler):

    def __init__(self, process_list: list[Process]):
        super().__init__(process_list)

    def do_schedule(self) -> Schedule:
        return self.schedule
