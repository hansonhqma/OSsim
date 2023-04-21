from process import Process
from heapq import *

class CPU:
    def __init__(self, context_switch_time:int,lamda: float, alpha:float):
        self.__tcs__ = context_switch_time
        self.__arrivalqueue__ = []
        self.lamda = lamda
        self.alpha = alpha
        self.time = 0

    def __printreadyqueue__(self, rdyq:list):
        if len(rdyq) == 0:
            return "[Q <empty>]"

        return "[Q " + " ".join([p[2].pid for p in sorted(rdyq, key = lambda x: (x[2].this_tau(), x[2].pid))]) + "]"

    def round_robin(self, process_list:list, quantum:int):
        pass
    
    def fcfs(self, process_list:list):
        print("time {}ms: Simulator started for FCFS {}".format( 0, self.__printreadyqueue__([])))
        [p.compute_predicted(self.lamda, self.alpha) for p in process_list]
        arrival_q = sorted(process_list, key=lambda p: (p.arrival_time,p.pid),  reverse=True)
        ready_q = []
        current_process = None
        next_burst_completion = 2**32
        while current_process or len(arrival_q) != 0 or len(ready_q) != 0:
            # Get all arrivals while before the next burst completion
            if len(arrival_q) > 0:
                while len(arrival_q) > 0 and arrival_q[-1].arrival_time <= next_burst_completion:
                    # Get next set of arrivals
                    next_arrivals = self.get_next_arrivals(arrival_q)
                    self.time = next_arrivals[0].arrival_time
                    # Add all arrivals to ready q
                    for p in next_arrivals:
                        heappush(ready_q, (p.arrival_time,p.pid, p))
                        if p.burst_index == 0:
                            print("time {}ms: Process {} arrived; added to ready queue {}".format(p.arrival_time, p.pid,  self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        else:
                            print("time {}ms: Process {} completed I/O; added to ready queue {}".format(p.arrival_time, p.pid,  self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    if not current_process:
                        # Context switch in as soon as the process arrives if nothing is in the CPU
                        self.time+= self.__tcs__//2
                        _, _, current_process = heappop(ready_q)
                        next_burst_completion = self.time + current_process.this_burst() 
                        print("time {}ms: Process {} started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_burst(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                # Complete this burst if there is a current process
                if current_process:
                    # Process finishes using the CPU and context switches with the next process
                    self.time = next_burst_completion 
                    old_tau = current_process.this_og_tau()
                    io_wait_time = current_process.this_io()
                    current_process.complete_this_burst()
                    # If this process is not finished, put somewhere in the arrival q
                    if not current_process.done():
                        # Indicate that this process has completed its burst
                        print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format( self.time, current_process.pid, current_process.remaining_bursts(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        # Context switch out of the cpu
                        print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(self.time, current_process.pid, self.time + self.__tcs__//2 + io_wait_time, self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        # Set new arrival time for process
                        current_process.arrival_time = self.time + io_wait_time + self.__tcs__//2
                        # Search for new chronological spot in arrival q from end
                        i = len(arrival_q) - 1
                        while i >= 0 and (current_process.arrival_time > arrival_q[i].arrival_time or (current_process.arrival_time == arrival_q[i].arrival_time and current_process.pid > arrival_q[i].pid)):
                            i-=1
                        arrival_q.insert(i+1, current_process)
                    else:
                        print("time {}ms: Process {} terminated {}".format(self.time, current_process.pid, self.__printreadyqueue__(ready_q)))
                    # Context switch out of CPU
                    self.time += self.__tcs__//2
                    current_process = None
            elif current_process:
                # Process finishes using the CPU and context switches with the next process
                self.time = next_burst_completion 
                old_tau = current_process.this_og_tau()
                io_wait_time = current_process.this_io()
                current_process.complete_this_burst()
                # If this process is not finished, put somewhere in the arrival q
                if not current_process.done():
                    # Indicate that this process has completed its burst
                    print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format( self.time, current_process.pid, current_process.remaining_bursts(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    # Context switch out of the cpu
                    print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(self.time, current_process.pid, self.time + self.__tcs__//2 + io_wait_time, self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    # Set new arrival time for process
                    current_process.arrival_time = self.time + io_wait_time + self.__tcs__//2
                    # Search for new chronological spot in arrival q from end
                    i = len(arrival_q) - 1
                    while i >= 0 and (current_process.arrival_time > arrival_q[i].arrival_time or (current_process.arrival_time == arrival_q[i].arrival_time and current_process.pid > arrival_q[i].pid)):
                        i-=1
                    arrival_q.insert(i+1, current_process)
                else:
                    print("time {}ms: Process {} terminated {}".format(self.time, current_process.pid, self.__printreadyqueue__(ready_q)))
                # Context switch out of CPU
                self.time += self.__tcs__//2
                current_process = None

            # Place next process in CPU
            if len(ready_q) > 0:
                self.time+= self.__tcs__//2
                _, _, current_process = heappop(ready_q)
                next_burst_completion = self.time + current_process.this_burst()
                print("time {}ms: Process {} started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
            else:
                next_burst_completion = 2**32
        print("time {}ms: Simulator ended for FCFS [Q <empty>]".format(self.time))
        self.time = 0
            


    def get_next_arrivals(self, arrival_q):
        next_arrivals = []
        next_arrival_time = arrival_q[-1].arrival_time
        while len(arrival_q) > 0 and arrival_q[-1].arrival_time == next_arrival_time:
            next_arrivals.append(arrival_q.pop())
        return next_arrivals

    def add_to_ready_q(self, processes, ready_q):
        for p in processes:
            heappush(ready_q, (p.this_tau(), p.pid, p))

    def shortest_job_first(self, process_list:list):
        print("time {}ms: Simulator started for SJF {}".format( 0, self.__printreadyqueue__([])))
        [p.compute_predicted(self.lamda, self.alpha) for p in process_list]
        arrival_q = sorted(process_list, key=lambda p: (p.arrival_time,p.pid),  reverse=True)
        ready_q = []
        current_process = None
        next_burst_completion = 2**32
        while current_process or len(arrival_q) != 0 or len(ready_q) != 0:
            # Get all arrivals while before the next burst completion
            if len(arrival_q) > 0:
                while len(arrival_q) > 0 and arrival_q[-1].arrival_time <= next_burst_completion:
                    # Get next set of arrivals
                    next_arrivals = self.get_next_arrivals(arrival_q)
                    self.time = next_arrivals[0].arrival_time
                    # Add all arrivals to ready q
                    for p in next_arrivals:
                        heappush(ready_q, (p.this_tau(), p.pid, p))
                        if p.burst_index == 0:
                            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format(p.arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        else:
                            print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(p.arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    if not current_process:
                        # Context switch in as soon as the process arrives if nothing is in the CPU
                        self.time+= self.__tcs__//2
                        _, _, current_process = heappop(ready_q)
                        next_burst_completion = self.time + current_process.this_burst() 
                        print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                # Complete this burst if there is a current process
                if current_process:
                    # Process finishes using the CPU and context switches with the next process
                    self.time = next_burst_completion 
                    old_tau = current_process.this_og_tau()
                    io_wait_time = current_process.this_io()
                    current_process.complete_this_burst()
                    # If this process is not finished, put somewhere in the arrival q
                    if not current_process.done():
                        # Indicate that this process has completed its burst
                        print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go {}".format( self.time, current_process.pid, old_tau, current_process.remaining_bursts(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        # Compute a new tau value
                        print("time {}ms: Recalculating tau for process {}: old tau {}ms ==> new tau {}ms {}".format( self.time, current_process.pid, old_tau, current_process.this_tau(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        # Context switch out of the cpu
                        print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(self.time, current_process.pid, self.time + self.__tcs__//2 + io_wait_time, self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        # Set new arrival time for process
                        current_process.arrival_time = self.time + io_wait_time + self.__tcs__//2
                        # Search for new chronological spot in arrival q from end
                        i = len(arrival_q) - 1
                        while i >= 0 and (current_process.arrival_time > arrival_q[i].arrival_time or (current_process.arrival_time == arrival_q[i].arrival_time and current_process.pid > arrival_q[i].pid)):
                            i-=1
                        arrival_q.insert(i+1, current_process)
                    else:
                        print("time {}ms: Process {} terminated {}".format(self.time, current_process.pid, self.__printreadyqueue__(ready_q)))
                    # Context switch out of CPU
                    self.time += self.__tcs__//2
                    current_process = None
            elif current_process:
                # Process finishes using the CPU and context switches with the next process
                self.time = next_burst_completion 
                old_tau = current_process.this_og_tau()
                io_wait_time = current_process.this_io()
                current_process.complete_this_burst()
                # If this process is not finished, put somewhere in the arrival q
                if not current_process.done():
                    # Indicate that this process has completed its burst
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go {}".format( self.time, current_process.pid, old_tau, current_process.remaining_bursts(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    # Compute a new tau value
                    print("time {}ms: Recalculating tau for process {}: old tau {}ms ==> new tau {}ms {}".format( self.time, current_process.pid, old_tau, current_process.this_tau(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    # Context switch out of the cpu
                    print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(self.time, current_process.pid, self.time + self.__tcs__//2 + io_wait_time, self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    # Set new arrival time for process
                    current_process.arrival_time = self.time + io_wait_time + self.__tcs__//2
                    # Search for new chronological spot in arrival q from end
                    i = len(arrival_q) - 1
                    while i >= 0 and (current_process.arrival_time > arrival_q[i].arrival_time or (current_process.arrival_time == arrival_q[i].arrival_time and current_process.pid > arrival_q[i].pid)):
                        i-=1
                    arrival_q.insert(i+1, current_process)
                else:
                    print("time {}ms: Process {} terminated {}".format(self.time, current_process.pid, self.__printreadyqueue__(ready_q)))
                # Context switch out of CPU
                self.time += self.__tcs__//2
                current_process = None

            # Place next process in CPU
            if len(ready_q) > 0:
                self.time+= self.__tcs__//2
                _, _, current_process = heappop(ready_q)
                next_burst_completion = self.time + current_process.this_burst()
                print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
            else:
                next_burst_completion = 2**32
        print("time {}ms: Simulator ended for SJF [Q <empty>]".format(self.time))
        self.time = 0

    def shortest_time_remaining(self, process_list: list):
        print("time {}ms: Simulator started for SRT {}".format( 0, self.__printreadyqueue__([])))
        [p.compute_predicted(self.lamda, self.alpha) for p in process_list]
        arrival_q = sorted(process_list, key=lambda p: (p.arrival_time,p.pid),  reverse=True)
        ready_q = []
        current_process = None
        next_burst_completion = 2**32
        while current_process or len(arrival_q) != 0 or len(ready_q) != 0:
            # Get all arrivals while before the next burst completion
            if len(arrival_q) > 0:
                while len(arrival_q) > 0 and arrival_q[-1].arrival_time <= next_burst_completion:
                    # Get next set of arrivals
                    next_arrivals = self.get_next_arrivals(arrival_q)
                    self.time = next_arrivals[0].arrival_time
                    if current_process:
                        current_process.run(current_process.this_burst() - (next_burst_completion-self.time))
                    # Add all arrivals to ready q and consider pre-emption
                    preempted = False
                    for p in next_arrivals:
                        if current_process and not preempted and (p.this_tau() < current_process.this_tau() or (p.this_tau() == current_process.this_tau() and p.pid < current_process.pid)):
                            # Pre-empt the current process
                            preempted = True
                            if p.burst_index == 0:
                                print("time {}ms: Process {} (tau {}ms) arrived; preempting {} {}".format(p.arrival_time, p.pid, p.this_tau(), current_process.pid, self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                            else:
                                print("time {}ms: Process {} (tau {}ms) completed I/O; preempting {} {}".format(p.arrival_time, p.pid, p.this_tau(), current_process.pid, self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                            heappush(ready_q, (current_process.this_tau(), current_process.pid, current_process))
                            current_process = None
                        else:
                            if p.burst_index == 0:
                                print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format(p.arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                            else:
                                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(p.arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        heappush(ready_q, (p.this_tau(), p.pid, p))
                    if preempted:
                        # Accunt for context switch from former process during preemption
                        self.time += self.__tcs__//2
                    if not current_process:
                        # Context switch in as soon as the process arrives if nothing is in the CPU
                        self.time+= self.__tcs__//2
                        _, _, current_process = heappop(ready_q)
                        next_burst_completion = self.time + current_process.this_burst() 
                        print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                # Complete this burst if there is a current process
                if current_process:
                    # Process finishes using the CPU and context switches with the next process
                    self.time = next_burst_completion 
                    old_tau = current_process.this_og_tau()
                    io_wait_time = current_process.this_io()
                    current_process.complete_this_burst()
                    # If this process is not finished, put somewhere in the arrival q
                    if not current_process.done():
                        # Indicate that this process has completed its burst
                        print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go {}".format( self.time, current_process.pid, old_tau, current_process.remaining_bursts(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        # Compute a new tau value
                        print("time {}ms: Recalculating tau for process {}: old tau {}ms ==> new tau {}ms {}".format( self.time, current_process.pid, old_tau, current_process.this_tau(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        # Context switch out of the cpu
                        print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(self.time, current_process.pid, self.time + self.__tcs__//2 + io_wait_time, self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                        # Set new arrival time for process
                        current_process.arrival_time = self.time + io_wait_time + self.__tcs__//2
                        # Search for new chronological spot in arrival q from end
                        i = len(arrival_q) - 1
                        while i >= 0 and (current_process.arrival_time > arrival_q[i].arrival_time or (current_process.arrival_time == arrival_q[i].arrival_time and current_process.pid > arrival_q[i].pid)):
                            i-=1
                        arrival_q.insert(i+1, current_process)
                    else:
                        print("time {}ms: Process {} terminated {}".format(self.time, current_process.pid, self.__printreadyqueue__(ready_q)))
                    # Context switch out of CPU
                    self.time += self.__tcs__//2
                    current_process = None
            elif current_process:
                # Process finishes using the CPU and context switches with the next process
                self.time = next_burst_completion 
                old_tau = current_process.this_og_tau()
                io_wait_time = current_process.this_io()
                current_process.complete_this_burst()
                # If this process is not finished, put somewhere in the arrival q
                if not current_process.done():
                    # Indicate that this process has completed its burst
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go {}".format( self.time, current_process.pid, old_tau, current_process.remaining_bursts(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    # Compute a new tau value
                    print("time {}ms: Recalculating tau for process {}: old tau {}ms ==> new tau {}ms {}".format( self.time, current_process.pid, old_tau, current_process.this_tau(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    # Context switch out of the cpu
                    print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(self.time, current_process.pid, self.time + self.__tcs__//2 + io_wait_time, self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
                    # Set new arrival time for process
                    current_process.arrival_time = self.time + io_wait_time + self.__tcs__//2
                    # Search for new chronological spot in arrival q from end
                    i = len(arrival_q) - 1
                    while i >= 0 and (current_process.arrival_time > arrival_q[i].arrival_time or (current_process.arrival_time == arrival_q[i].arrival_time and current_process.pid > arrival_q[i].pid)):
                        i-=1
                    arrival_q.insert(i+1, current_process)
                else:
                    print("time {}ms: Process {} terminated {}".format(self.time, current_process.pid, self.__printreadyqueue__(ready_q)))
                # Context switch out of CPU
                self.time += self.__tcs__//2
                current_process = None

            # Place next process in CPU
            if len(ready_q) > 0:
                self.time+= self.__tcs__//2
                _, _, current_process = heappop(ready_q)
                next_burst_completion = self.time + current_process.this_burst()
                print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q))) if self.time <= 9999 else None
            else:
                next_burst_completion = 2**32
        print("time {}ms: Simulator ended for SRT [Q <empty>]".format(self.time))
        self.time = 0 

    


            
