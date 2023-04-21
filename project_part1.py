# CSCI 4210 OS Simulation project part 1
# 
# Contrubibutors:
# - mah11@rpi.edu
# - baught@rpi.edu
# - malikr3@rpi.edu


import sys
from generator import Generator
from process import Process
from string import ascii_uppercase as process_id_set

__ERROR_PROMPT = "python3 project.py <n_proc: int> <n_cpu: int> <seed: int> <lambda: float> <ubound: int>"


if __name__ == '__main__':
    # exec arg validation
    if not len(sys.argv) == 6:
        print("ERROR: USAGE:", __ERROR_PROMPT)
        exit(1)

    # Runtime vars
    n_processes = 0
    n_cpu = 0
    rand48_seed = 0
    exp_lambda = 0.0
    exp_ubound = 0
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

    if n_cpu > n_processes:
        print("ERROR: n_proc >= n_cpu")
        exit(1)

    # rand
    gen = Generator(exp_lambda, exp_ubound, rand48_seed)
    print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound {} >>>".format(n_processes, n_cpu, "process" if n_cpu == 1 else "processes" ))
    
    processes = [] 
    for i in range(n_processes):
        io_bound = i < n_processes - n_cpu
        
        p = gen.next_process(io_bound, process_id_set[i])
        
        if p:
            processes.append(p)
        else:
            i-=1
    
    for i in range(len(processes)):
        processes[i].print() 
