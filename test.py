import time
import os
wait_time = 3
n_processes = 2

def comparePaths(path1, path2):
    if(path1 == path2):
        return True
    else:
        return False
    
def printPaths(parallel, sequential):
    print("Parallel path\n", parallel)
    print("Sequential path\n", sequential)

# Checks if the path is the right one 
# based on the path stored in variables
def test0(parallel):
    from variables import right_answer
    if(parallel != right_answer):
        print("\nThe parallel program didn't find the right answer.")
    else:
        print("\nThe parallel program found the right answer.")
    
# Checks if both paths are equal
def test1(sequential, parallel):
    if(comparePaths(parallel, sequential)):
        print("\nBoth paths are equal.\n")
    else:
        print("\nBoth paths are not equal\n.")

# Checks the timings of both programms
def test2(s_time, p_time):
    time_dif = abs(p_time - s_time)
    ideal_time = s_time/n_processes
    speedup = s_time/p_time
    efficiency = speedup/n_processes
    
    print(f"Parallel found the path in {p_time} seconds.")
    print(f"Sequential found the path in {s_time} seconds.\n")
    
    print(f"The time execution of the parallel program was {'faster' if p_time < s_time else 'slower'} by {time_dif} seconds.")
    print(f"The speedup of the parallel program is {speedup}X.\n")
    
    print(f"The ideal time for {n_processes} processes is equal to {ideal_time} seconds.")
    
    print(f"This means that the parallel program is {'superlinear' if p_time < ideal_time else 'sublinear'}")
    print(f"since the time of the parallel program was {'less' if p_time < ideal_time else 'greater'} than the ideal time.\n")
    
    print(f"The efficiency of the program is {efficiency}.")

def main():
    
    os.system("python3 sequential.py")
    os.system("python3 parallel.py")
    
    time.sleep(wait_time)
    
    from parallel_result import path as parallel, time as p_time
    from sequential_result import path as sequential, time as s_time
   
    # printPaths(parallel, sequential)

    # Test 0 shouldn't be used if variables file is not used.  
    test0(parallel)
    test1(sequential, parallel)    
    test2(s_time, p_time)
        

if __name__ == '__main__':
    main()