class Schedule:
    """
    scheduler may return construct and return this object to
    gantt chart drawer in order to draw chart based on the information
    process_name -> which process
    time_out -> occupied the cpu from last_time_out till time_out
    """
    def __init__(self):
        self.schedule = []

    def add_schedule(self, process_name: str, time_out: int | float):
        self.schedule.append((process_name, time_out))