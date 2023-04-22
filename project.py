# CSCI 4210 OS Simulation project part 2
# 
# Contrubibutors:
# - mah11@rpi.edu
# - baught@rpi.edu
# - malikr3@rpi.edu


import sys
from generator import Generator
from cpu import CPU
from string import ascii_uppercase as process_id_set

__ERROR_PROMPT__ = "python3 project.py <n_proc: int> <n_cpu: int> <seed: int> <lambda: float> <ubound: int> <tcs: int> <alpha: float> <tslice: int>"


if __name__ == '__main__':
    # exec arg validation
    if not len(sys.argv) == 9:
        print("ERROR: USAGE:", __ERROR_PROMPT__)
        exit(1)

    # Runtime vars
    n_processes = 0
    n_cpu = 0
    rand48_seed = 0
    exp_lambda = 0.0
    exp_ubound = 0
    tcs = 0
    alpha = 0
    tslice = 0
    
    try:
        n_processes = int(sys.argv[1])
    except:
        print("ERROR: n_processes should be an integer.")
        exit(1)
    try:
        n_cpu = int(sys.argv[2])
    except:
        print("ERROR: n_cpu should be an integer.")
        exit(1)
    try:
        rand48_seed = int(sys.argv[3])
    except:
        print("ERROR: rand48_seed should be an integer.")
        exit(1)
    try:
        exp_lambda = float(sys.argv[4])
    except:
        print("ERROR: exp_lambda should be a float/double.")
        exit(1)
    try:
        exp_ubound = int(sys.argv[5])
    except:
        print("ERROR: exp_ubound should be an integer.")
        exit(1)
    try:
        tcs = int(sys.argv[6])
    except:
        print("ERROR: tcs shoudl be an integer")
        exit(1)
    
    try:
        alpha = float(sys.argv[7])
    except:
        print("ERROR: alpha should be float")
        exit(1)
    
    try:
        tslice = int(sys.argv[8])
    except:
        print("ERROR: tslice should be int")
        exit(1)

    if n_cpu > n_processes:
        print("ERROR: n_proc >= n_cpu")
        exit(1)

    # rand
    # Fuck it
    gen1 = Generator(exp_lambda, exp_ubound, rand48_seed)
    gen2 = Generator(exp_lambda, exp_ubound, rand48_seed)
    gen3 = Generator(exp_lambda, exp_ubound, rand48_seed)
    gen4 = Generator(exp_lambda, exp_ubound, rand48_seed)
    
    processes1 = [] 
    processes2 = [] 
    processes3 = [] 
    processes4 = [] 
    for i in range(n_processes):
        io_bound = i < n_processes - n_cpu
        
        p1 = gen1.next_process(io_bound, process_id_set[i])
        p2 = gen2.next_process(io_bound, process_id_set[i])
        p3 = gen3.next_process(io_bound, process_id_set[i])
        p4 = gen4.next_process(io_bound, process_id_set[i])
        
        if p1:
            processes1.append(p1)
            processes2.append(p2)
            processes3.append(p3)
            processes4.append(p4)
        else:
            i-=1

    print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound {} >>>".format(n_processes, n_cpu, "process" if n_cpu == 1 else "processes" ))
    for i in range(len(processes1)):
        print(processes1[i])

    print("\n<<< PROJECT PART II -- t_cs={}ms; alpha={}; t_slice={}ms >>>".format(tcs, alpha, tslice))
    # built processes array
    
    cpu = CPU(tcs, exp_lambda, alpha)
    
    # Fuck it
    # run algorithms
    #cpu.fcfs(processes1)
    #print()
    #cpu.shortest_job_first(processes2)
    #print()
    cpu.shortest_time_remaining(processes3)
    #print()
   # cpu.round_robin(processes4, tslice)