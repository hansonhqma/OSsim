import rand
import math
from process import Process

class Generator(object):
    def __init__(self, lamda: int, ubound:int, seed: int):
        self.lamda = lamda
        self.engine = rand.rand48(seed)
        self.ubound = ubound

    def next_exp(self) -> float:
        """
        exponential distribution as a function of random variable r
        if next_exp > self.ubound, we continue generating numbers until we find one <= self.ubound
        """

        # uniform random variable to exponential
        out = self.ubound+1
        while(out > self.ubound):
            out = -math.log(self.engine.drand48()) / self.lamda
        return out
    
    def next_process(self, io_bound:bool):
        """
        @returns if next_exp() >= 0
                    new Process P with an initial arrival time and a number of cpu bursts, each of which
                    has the same burst time. All io wait times for the process also have the same value.
                 else:
                    None 
                    TODO: Should we instead return a trivial process, i.e. Process(0, 0, 0, 0)?
        """
        initial_arrival_time = math.floor(self.next_exp())
        if initial_arrival_time > self.ubound:
            return None
        cpu_bursts = math.ceil(100 * self.engine.drand48())
        intervals = []
        for _ in range(cpu_bursts - 1):
            cpu_burst_time = math.ceil(self.next_exp())
            io_time = math.ceil(self.next_exp()) * 10
            # TODO: Multiply by 10 if a CPU_BOUND process?
            if not io_bound:
                cpu_burst_time*=4
                io_time/=4
            intervals.append(cpu_burst_time)
            intervals.append(io_time)

        cpu_burst_time = math.ceil(self.next_exp())
        if not io_bound:
           cpu_burst_time*=4
        intervals.append(cpu_burst_time)

        return Process(initial_arrival_time, cpu_bursts, intervals, io_bound)
        
        


        
    
