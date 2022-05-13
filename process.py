"""
Define Process class

Process class will be instantiated with following attributes

process_ID(str)         : name of the process; P1 P2 etc...; must be denoted at the Gantt Chart
arrival_time(int)       : arrival time of the process; larger than 0
service_time(int)       : required cpu burst time to give user the first response; le 0(?)
priority(int)           : priority of the process; le 0; smaller number means higher priority
cpu_burst_time(int)     : required cpu burst time of process; larger than 0

attributes above are stated in the document provided in class
following attributes are made for convenience - based on personal opinion
thus, can be modified at any time

last_time_out(int)      : stores time when the process was context switched by the scheduler;
                          can be used to compute WT, TT
time_left(int)          : stores required cpu burst time to complete the process;
                          initialized same as cpu_burst_time;
                          can be used to compute WT, TT, RT
wait_time(int)          : stores time the process was in the ready queue; WT itself
response_time(int)      : actual response time; RT itself
turnaround_time(int)    : stores time when the process was done; TT itself

process_complete(bool)  : flag used to check whether the process is finished
"""

from utils import WrongCpuBurstTimeError, TimeMismatchError, CompletedProcessAgainError

class Process:

    def __init__(self, process_ID: str, arrival_time: int, service_time: int, priority: int, cpu_burst_time: int):
        self.process_ID = process_ID
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.cpu_burst_time = cpu_burst_time
        self.priority = priority

        self.last_time_out = self.arrival_time
        self.time_left = self.cpu_burst_time

        self.wait_time = 0
        self.response_time = -1
        self.turnaround_time = -1

        self.process_complete = False

    def use_cpu(self, allocated_burst_time: int, current_time: int):
        """
        :param allocated_burst_time: passed from scheduler, time using cpu, int
        :param current_time: passed from scheduler, current time, when process start using the cpu
        :return None

        scheduler will sort the list of the process according to its property(FCFS by arrival time etc...)
        or simulate scheduling according to its property(maybe RR?)

        then it pop out the process from the ready queue and just use this method in order to use cpu
        process.use_cpu(allocated_burst_time, current_time)

        all WT RT TT can be computed in this function.
        """
        # Error occurs when your scheduler allocate CPU to finished process
        if self.process_complete:
            raise CompletedProcessAgainError(current_time, self.turnaround_time)

        # Error occurs when your scheduler allocate CPU to process not arrived yet
        if self.arrival_time > current_time:
            raise TimeMismatchError(current_time, self.arrival_time)

        # Error occurs when your scheduler allocate excessive cpu burst time to the process
        if allocated_burst_time > self.time_left:
            raise WrongCpuBurstTimeError(allocated_burst_time, self.time_left)

        # compute wait time and add it up to wait_time
        if current_time - self.last_time_out < 0:
            raise TimeMismatchError(current_time, self.last_time_out)
        self.wait_time += current_time - self.last_time_out

        # check if response happened, if it did, store it to response time
        if self.response_time == -1 and self.service_time <= (self.cpu_burst_time - self.time_left) + allocated_burst_time:
            self.response_time = current_time + self.service_time - (self.cpu_burst_time - self.time_left)

        # use cpu and modify last_time_out
        self.time_left -= allocated_burst_time
        self.last_time_out = current_time + allocated_burst_time

        # check if process is completed, if it did, compute TT and mark process_done flag True
        if self.time_left == 0:
            self.turnaround_time = self.last_time_out - self.arrival_time
            self.process_complete = True

    def get_result(self) -> dict:
        """
        :return result: dictionary which contains PID, WT, RT, TT
        """
        result = {"PID": self.process_ID, "WT": self.wait_time, "RT": self.response_time, "TT": self.turnaround_time}
        return result
