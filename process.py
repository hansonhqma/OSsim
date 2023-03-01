from copy import deepcopy

class Process(object):
    def __init__(self, arrival_time: int, cpu_bursts: int, intervals: list, io_bound:bool):
        self.arrival_time = arrival_time
        self.cpu_bursts = cpu_bursts
        self.intervals = deepcopy(intervals)
        self.io_bound = io_bound
    def print(self, process_name: str):
        print("{}-bound process {}: arrival time {}ms; {} CPU bursts:".format("I/O" if self.io_bound else "CPU", process_name, self.arrival_time, self.cpu_bursts))
        for i in range(0, len(self.intervals) - 1):
            if i%2 == 0:
                print("--> CPU burst {}ms".format(self.intervals[i]), end = " ")
            
            else:
                print("--> I/O burst {}ms".format(self.intervals[i]))
        print("--> CPU burst {}ms".format(self.intervals[-1]))
        

