from process import Process


class CPU:
    def __init__(self, context_switch_time:int):
        self.__tcs__ = context_switch_time
        self.__arrivalqueue__ = []

    def __printreadyqueue__(self, rdyq:list[Process]):
        if len(rdyq) == 0:
            return "[Q <empty>]"

        return "[Q " + " ".join([p.pid for p in rdyq]) + "]"

    def round_robin(self, process_list:list[Process], quantum:int):
        pass
    
    def fcfs(self, process_list:list[Process]):
        # sort processes by arrival time for arrival queue
        self.__arrivalqueue__ = sorted(process_list, key=lambda p:p.arrival_time)
        readyqueue = []

        pass
    
    def shortest_time_remaining(self, process_list:list[Process]):
        pass
    
    def shortest_job_first(self, process_list:list[Process]):
        pass