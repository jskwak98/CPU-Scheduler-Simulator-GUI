from abc import *

from process import Process
from utils import Schedule

class Scheduler(metaclass=ABCMeta):
    """
    Abstract Scheduler class which can be used as parent class for each schedulers

    common attributes are process_list, which is list of Process objects
    and schedule, which is a Schedule object
    """
    def __init__(self, process_list: list[Process]):
        self.process_list = process_list
        self.schedule = Schedule()

    @abstractmethod
    def do_schedule(self) -> Schedule:
        pass
