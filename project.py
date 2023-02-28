# CSCI 4210 OS Simulation project part 1
# 
# Contrubibutors:
# - mah11@rpi.edu
# - 
# - 


import sys
import rand
from string import ascii_uppercase as process_id_set

__ERROR_PROMPT = 'python3 project.py <n_proc> <n_cpu> <seed> <lambda> <ubound>'


if __name__ == '__main__':
    

    # exec arg validation
    if not len(sys.argv) == 6:
        raise RuntimeError(__ERROR_PROMPT)

    # Runtime vars
    n_processes = int(sys.argv[1])
    n_cpu = int(sys.argv[2])
    rand48_seed = int(sys.argv[3])
    exp_lambda = float(sys.argv[4])
    exp_ubound = float(sys.argv[5])

    if n_cpu > n_processes:
        print("n_proc >= n_cpu")
        raise RuntimeError(__ERROR_PROMPT)


    # rand
    rand48_engine = rand.rand48(rand48_seed)

    print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound process >>>".format(n_processes, n_cpu))
    
    
    for proc_index in range(n_processes):
        proc_id = process_id_set[proc_index]

        io_bound = proc_index < n_processes - n_cpu

        if io_bound:
            pass

        else:
            pass
    
