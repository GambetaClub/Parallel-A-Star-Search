import time
from subprocess import Popen
 
def comparePaths(path1, path2):
    if(path1 == path2):
        return True
    else:
        return False
    
def test1(parallel, sequential):
    if(comparePaths(parallel, sequential)):
        print("\nBoth paths are equal.")
    else:
        print("\nBoth paths are not equalt.")

def test2(p_time, s_time):
    print(f"\nParallel found the path in {p_time} seconds")
    print(f"\nSequential found the path in {s_time} seconds")
    
    time_dif = abs(p_time - s_time)
    if(p_time > s_time):
        print(f"The time execution of the parallel program was slower by {time_dif} seconds.")
    else:
        print(f"The time execution of the parallel program was faster by {time_dif} seconds.")

def main():

    Popen('python sequential.py')
    Popen('python parallel.py')
    
    time.sleep(3)
    
    from parallel_result import path as parallel, time as p_time
    from sequential_result import path as sequential, time as s_time
    
    test1(parallel, sequential)    
    test2(p_time, s_time)
        

if __name__ == '__main__':
    main()