from copy import deepcopy

class Process(object):
    
    def __init__(self, arrival_time: int, cpu_bursts: int, intervals: list, io_bound:bool, pid:str):
        # arrival time in ms
        # number is intervals is cpu bursts * 2 - 1, since every cpu burst is interrupted by an io burst
        # -> processing goes cpu, io, cpu, io, ...., io, cpu
        
        self.arrival_time = arrival_time
        self.cpu_bursts = cpu_bursts
        self.intervals = deepcopy(intervals)
        self.io_bound = io_bound
        self.pid = pid
        
    def print(self):
        print("{}-bound process {}: arrival time {}ms; {} CPU bursts:".format("I/O" if self.io_bound else "CPU", self.pid, self.arrival_time, self.cpu_bursts))
        for i in range(0, len(self.intervals) - 1):
            if i%2 == 0:
                print("--> CPU burst {}ms".format(self.intervals[i]), end = " ")
            
            else:
                print("--> I/O burst {}ms".format(self.intervals[i]))
        print("--> CPU burst {}ms".format(self.intervals[-1]))
        
    def __str__(self):
        return "{}-bound process {}: arrival time {}ms; {} CPU bursts".format(\
            "I/O" if self.io_bound else "CPU", self.pid, self.arrival_time, self.cpu_bursts)
        

