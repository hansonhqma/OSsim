from process import Process
from heapq import *

class CPU:
    def __init__(self, context_switch_time:int,lamda: float, alpha:float):
        self.__tcs__ = context_switch_time
        self.__arrivalqueue__ = []
        self.lamda = lamda
        self.alpha = alpha
        self.time = 0

    def __printreadyqueue__(self, rdyq:list[Process]):
        if len(rdyq) == 0:
            return "[Q <empty>]"

        return "[Q " + " ".join([p[2].pid for p in sorted(rdyq, key = lambda x: (x[2].this_tau(), x[2].pid))]) + "]"

    def round_robin(self, process_list:list[Process], quantum:int):
        pass
    
    def fcfs(self, process_list:list[Process]):
        # sort processes by arrival time for arrival queue
        self.__arrivalqueue__ = sorted(process_list, key=lambda p:p.arrival_time)
        readyqueue = []

        pass

    def get_next_arrivals(self, arrival_q):
        next_arrivals = []
        next_arrival_time = arrival_q[-1].arrival_time
        while len(arrival_q) > 0 and arrival_q[-1].arrival_time == next_arrival_time:
            next_arrivals.append(arrival_q.pop())
        return next_arrivals

    def add_to_ready_q(self, processes, ready_q):
        for p in processes:
            heappush(ready_q, (p.this_tau(), p.pid, p))

    def shortest_time_remaining(self, process_list:list[Process]):
        print("time {}ms: Simulator started for SRT {}".format( 0, self.__printreadyqueue__([])))
        [p.compute_predicted(self.lamda, self.alpha) for p in process_list]
        arrival_q = sorted(process_list, key=lambda p: (p.arrival_time,p.pid),  reverse=True)
        ready_q = []
        current_process = None
        while len(arrival_q) != 0 or len(ready_q) != 0:
            # Process this burst until next arrival time
            next_arrival_time = None
            if len(arrival_q) > 0:
                next_arrival_time = arrival_q[-1].arrival_time
            else:
                next_arrival_time = 2**32
            # Do all work before next arrival
            if current_process:
                # Do work for this process
                actual_burst_completion_time = self.time + current_process.this_burst()
                # If this burst goes beyond the next arrival time, do all the work until that time
                if actual_burst_completion_time > next_arrival_time:
                    # Consume time in CPU until next arrival
                    current_process.run(next_arrival_time - self.time)
                    self.time = next_arrival_time 
                    # Check if one of next arrivals pre-empt this process
                    next_arrivals = self.get_next_arrivals(arrival_q)
                    # Sort next_arrivals by predicted burst time
                    next_arrivals.sort(key = lambda p: (p.this_tau(), p.pid))
                    # Check if first element in next_arrivals can pre-empt the current process
                    preempted = False
                    if next_arrivals[0].this_tau() < current_process.this_tau() or (next_arrivals[0].this_tau() == current_process.this_tau() and next_arrivals[0].pid < current_process.pid):
                        # Perform pre-emption
                        if next_arrivals[0].burst_index == 0:
                            print("time {}ms: Process {} (tau {}ms) arrived; preempting {} {}".format( self.time, next_arrivals[0].pid, next_arrivals[0].this_tau(),current_process.pid, self.__printreadyqueue__(ready_q)))
                        else:
                            print("time {}ms: Process {} (tau {}ms) completed I/O; preempting {} {}".format( self.time, next_arrivals[0].pid, next_arrivals[0].this_tau(),current_process.pid, self.__printreadyqueue__(ready_q)))
                        
                    # Add all new arrivals to ready q and check for pre-emption
                    for i in range(preempted, len(next_arrivals)):
                        p = next_arrivals[i]
                        heappush(ready_q, (p.this_tau(), p.pid, p))
                        if p.burst_index == 0:
                            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format( next_arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q)))
                        else:
                            print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format( next_arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q)))
                    # Context switch out and switch in the new process if a pre-emption occurred
                    if preempted:
                        # Context switch out old process
                        self.time+=self.__tcs__//2
                        # Place on ready queue
                        heappush(ready_q, (current_process.this_tau(), current_process.pid, current_process))
                        # Context switch in the new process
                        current_process = next_arrivals[0]
                        self.time+=self.__tcs__//2
                        print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q)))

                elif actual_burst_completion_time <= next_arrival_time:
                    # Do work for as many processes as possible before next arrival time
                    while current_process and actual_burst_completion_time <= next_arrival_time:
                        # Process finishes using the CPU and context switches with the next process
                        self.time += current_process.this_burst()
                        old_tau = current_process.this_og_tau()
                        io_wait_time = current_process.this_io()
                        current_process.complete_this_burst()
                        # If this process is not finished, put somewhere in the arrival q
                        if not current_process.done():
                            # Indicate that this process has completed its burst
                            print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go {}".format( self.time, current_process.pid, old_tau, current_process.remaining_bursts(), self.__printreadyqueue__(ready_q)))
                            # Compute a new tau value
                            print("time {}ms: Recalculating tau for process {}: old tau {}ms ==> new tau {}ms {}".format( self.time, current_process.pid, old_tau, current_process.this_tau(), self.__printreadyqueue__(ready_q)))
                            # Context switch out of the cpu
                            print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(self.time, current_process.pid, self.time + self.__tcs__//2 + io_wait_time, self.__printreadyqueue__(ready_q)))
                            # Set new arrival time for process
                            current_process.arrival_time = self.time + io_wait_time + self.__tcs__//2
                            # Search for new chronological spot in arrival q from end
                            i = len(arrival_q) - 1
                            while i >= 0 and (current_process.arrival_time > arrival_q[i].arrival_time or (current_process.arrival_time == arrival_q[i].arrival_time and current_process.pid > arrival_q[i].pid)):
                                i-=1
                            # If the current process's next arrival time is earlier than our current one, change it
                            if current_process.arrival_time < next_arrival_time:
                                next_arrival_time = current_process.arrival_time
                            arrival_q.insert(i+1, current_process)
                        else:
                            print("time {}ms: Process {} terminated {}".format(self.time, current_process.pid, self.__printreadyqueue__(ready_q)))
                        self.time += self.__tcs__//2

                        
                        # New process context switches into CPU
                        if len(ready_q) == 0:
                            current_process = None
                            break
                        _, _, current_process = heappop(ready_q)
                        self.time+= self.__tcs__//2
                        print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q)))
                        actual_burst_completion_time = self.time + current_process.this_burst() 

                    # Get all arrivals at next arrival time 
                    if current_process:
                        current_process.run(next_arrival_time - self.time)
                        self.time = next_arrival_time
                        # Check if one of next arrivals pre-empt this process
                        next_arrivals = self.get_next_arrivals(arrival_q)
                        # Sort next_arrivals by predicted burst time
                        next_arrivals.sort(key = lambda p: (p.this_tau(), p.pid))
                        # Check if first element in next_arrivals can pre-empt the current process
                        preempted = False
                        if next_arrivals[0].this_tau() < current_process.this_tau() or (next_arrivals[0].this_tau() == current_process.this_tau() and next_arrivals[0].pid < current_process.pid):
                            # Perform pre-emption
                            if next_arrivals[0].burst_index == 0:
                                print("time {}ms: Process {} (tau {}ms) arrived; preempting {} {}".format( self.time, next_arrivals[0].pid, next_arrivals[0].this_tau(),current_process.pid, self.__printreadyqueue__(ready_q)))
                            else:
                                print("time {}ms: Process {} (tau {}ms) completed I/O; preempting {} {}".format( self.time, next_arrivals[0].pid, next_arrivals[0].this_tau(),current_process.pid, self.__printreadyqueue__(ready_q)))
                            preempted = True
                            
                        # Add all new arrivals to ready q and check for pre-emption
                        for i in range(preempted, len(next_arrivals)):
                            p = next_arrivals[i]
                            heappush(ready_q, (p.this_tau(), p.pid, p))
                            if p.burst_index == 0:
                                print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format( next_arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q)))
                            else:
                                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format( next_arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q)))
                        # Context switch out and switch in the new process if a pre-emption occurred
                        if preempted:
                            # Context switch out old process
                            self.time+=self.__tcs__//2
                            # Place on ready queue
                            heappush(ready_q, (current_process.this_tau(), current_process.pid, current_process))
                            # Context switch in the new process
                            current_process = next_arrivals[0]
                            self.time+=self.__tcs__//2
                            print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q)))
                    else:
                        self.time = next_arrival_time
                        next_arrivals = self.get_next_arrivals(arrival_q)
                        for p in next_arrivals:
                            heappush(ready_q, (p.this_tau(), p.pid, p))
                            if p.burst_index == 0:
                                print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format( next_arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q)))
                            else:
                                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format( next_arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q)))
            else:
                # If no process is currently in the CPU
                if len(ready_q) > 0:
                    # Try to get one from the ready q 
                    # Context switch into CPU
                    _, _, current_process = heappop(ready_q)
                    self.time += self.__tcs__//2
                    print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format( self.time, current_process.pid, current_process.this_tau(),current_process.this_burst(), self.__printreadyqueue__(ready_q)))
                else:
                    # Otherwise, just go to next set of arrivals
                    self.time = next_arrival_time 
                    # Get all arrivals at this time
                    next_arrivals = self.get_next_arrivals(arrival_q)
                    for p in next_arrivals:
                        heappush(ready_q, (p.this_tau(), p.pid, p))
                        if p.burst_index == 0:
                            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format( next_arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q)))
                        else:
                            print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format( next_arrival_time, p.pid, p.this_tau(), self.__printreadyqueue__(ready_q)))

                
                


            

    def shortest_job_first(self, process_list:list[Process]):
        pass