"""
Define Process class

Process class will be instantiated with following attributes

process_name(str)       : name of the process; P1 P2 etc...; must be denoted at the Gantt Chart
arrival_time(numeric)   : arrival time of the process; larger than 0
cpu_burst_time(numeric) : required cpu burst time of process; larger than 0
first_response(numeric) : required cpu burst time to give user the first response; le 0(?)
priority(int)           : priority of the process; le 0; smaller number means higher priority

attributes above are stated in the document provided in class
following attributes are made for convenience - based on personal opinion
thus, can be modified at any time

last_time_out(numeric)  : stores time when the process was context switched by the scheduler;
                          can be used to compute WT, TT
time_left(numeric)      : stores required cpu burst time to complete the process;
                          initialized same as cpu_burst_time;
                          can be used to compute WT, TT, RT
cumulative_wt(numeric)  : stores time the process was in the ready queue; WT itself
response_time(numeric)  : actual response time
"""

class Process:

    def __init__(self, process_name, arrival_time, cpu_burst_time, first_response, priority):
        self.process_name = process_name
        self.arrival_time = arrival_time
        self.cpu_burst_time = cpu_burst_time
        self.first_response = first_response
        self.priority = priority

        self.last_time_out = -1
        self.time_left = self.cpu_burst_time
        self.cumulative_wt = 0
        self.response_time = -1

    def use_cpu(self, time_used, current_time):
        """
        :param time_used: passed from scheduler, time using cpu, numeric
        :param current_time: passed from scheduler, current time
        :return(?) process_done: boolean flag notifying if the process is complete or not

        scheduler will sort the list of the process according to its property(FCFS by arrival time etc...)
        or simulate scheduling according to its property(maybe RR?)

        then it pop out the process from the ready queue and just use this method in order to use cpu
        process.use_cpu(time_used, current_time)

        all WT RT TT can be computed in this function.
        """
        pass

    def get_result(self):
        """
        :return result: RT, WT, TT, maybe can define class for this in utils.py, or just use tuple
        """
        pass