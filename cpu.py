
class CPU:
    def __init__(self, context_switch_time:int):
        self.__tcs__ = context_switch_time
        
    def round_robin(self, process_list:list, quantum:int):
        pass
    
    def fcfs(self, process_list:list):
        pass
    
    def shortest_time_remaining(self, process_list:list):
        pass
    
    def shortest_job_first(self, process_list:list):
        pass