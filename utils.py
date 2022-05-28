class Schedule:
    """
    scheduler may return construct and return this object to
    gantt chart drawer in order to draw chart based on the information
    process_name -> which process
    time_out -> occupied the cpu from last_time_out till time_out
    """
    def __init__(self):
        self.schedule = []


    def add_schedule(self, process_name: str, time_out: int):
        if self.schedule and self.schedule[-1][0] == process_name:
            self.schedule.pop()
        self.schedule.append((process_name, time_out))


class WrongCpuBurstTimeError(Exception):
    """
    Error Defined for convenience - might be useful for RR
    if your scheduler allocate more cpu time than the process's left cpu burst time to the process, this error is raised
    Just for debugging
    """
    def __init__(self, scheduler_cpu_burst_time: int, currently_left_time: int):
        self.scheduler_cpu_burst_time = scheduler_cpu_burst_time
        self.currently_left_time = currently_left_time

    def __str__(self):
        return f"잘못된 Burst Time 입력입니다. 프로세스의 남은 Burst Time : {self.currently_left_time}, " \
               f"스케쥴러가 정한 Burst Time : {self.scheduler_cpu_burst_time}"


class TimeMismatchError(Exception):
    """
    if your scheduler's time and process's time is unmatching
    can happen if you add up time of your scheduler incorrectly
    Just for debugging
    """
    def __init__(self, scheduler_time: int, process_time: int, e_type: int = 1):
        self.scheduler_time = scheduler_time
        self.process_time = process_time
        self.e_type = e_type

    def __str__(self):
        if self.e_type == 0:
            return f"아직 도착하지 않은 프로세스에 CPU 할당. 스케쥴러의 현 시각 : {self.scheduler_time}, " \
               f"프로세스 arrival time : {self.process_time}"
        else:
            return f"스케쥴러의 시각은 반드시 프로세스가 최근 CPU를 사용한 시각보다 크거나 같아야 합니다. 스케쥴러의 현 시각 : {self.scheduler_time}, " \
                   f"프로세스가 CPU에서 나온 가장 최근 시각 : {self.process_time}"


class CompletedProcessAgainError(Exception):
    """
    it sounds funny, but it may happen
    error occurs when your scheduler somehow try to allocate CPU to finished process.
    check if your queue or some kind of fringe object is correctly popping finished process.
    """
    def __init__(self, scheduler_time: int, process_time: int):
        self.scheduler_time = scheduler_time
        self.process_time = process_time


    def __str__(self):
        return f"이미 작업이 완료된 프로세스를 재할당하려 합니다. 스케쥴러의 현 시각 : {self.scheduler_time}, " \
               f"프로세스가 CPU 작업을 마친 시각 : {self.process_time}"