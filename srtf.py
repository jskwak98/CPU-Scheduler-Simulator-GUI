from scheduler import Scheduler
from utils import Schedule
from process import Process


class srtf():
    def __init__(self, process_list: list[Process]):
        self.process_list = process_list

    def do_schedule(self, process_list):
        start_time = []
        exit_time = []
        s_time = 0
        gant = []
        process_list.sort(key=lambda x: x[1])
        '''
        Sort processes according to the Arrival Time
        '''
        while 1:
            ready_queue = []
            normal_queue = []
            temp = []
            for i in range(len(process_list)):
                if process_list[i][1] <= s_time and process_list[i][3] == 0:
                    temp.extend([process_list[i][0], process_list[i][1], process_list[i][2], process_list[i][4]])
                    ready_queue.append(temp)
                    temp = []
                elif process_list[i][3] == 0:
                    temp.extend([process_list[i][0], process_list[i][1], process_list[i][2], process_list[i][4]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                '''
                Sort processes according to Burst Time
                '''
                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                gant.append(ready_queue[0][0])
                for k in range(len(process_list)):
                    if process_list[k][0] == ready_queue[0][0]:
                        break
                process_list[k][2] = process_list[k][2] - 1
                if process_list[k][2] == 0:  # If Burst Time of a process is 0, it means the process is completed
                    process_list[k][3] = 1
                    process_list[k].append(e_time)
            if len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                gant.append(normal_queue[0][0])
                for k in range(len(process_list)):
                    if process_list[k][0] == normal_queue[0][0]:
                        break
                process_list[k][2] = process_list[k][2] - 1
                if process_list[k][2] == 0:  # If Burst Time of a process is 0, it means the process is completed
                    process_list[k][3] = 1
                    process_list[k].append(e_time)

        total_turnaround_time = 0
        for i in range(len(process_list)):
            turnaround_time = process_list[i][5] - process_list[i][1]
            '''
            turnaround_time = completion_time - arrival_time
            '''
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_list[i].append(turnaround_time)
        average_turn = total_turnaround_time / len(process_list)

        total_waiting_time = 0
        for i in range(len(process_list)):
            waiting_time = process_list[i][6] - process_list[i][4]
            '''
            waiting_time = turnaround_time - burst_time
            '''
            total_waiting_time = total_waiting_time + waiting_time
            process_list[i].append(waiting_time)
        average_wait = total_waiting_time / len(process_list)


        return self.process_list, average_wait, average_turn, gant