import math
import random
import time
import sys

def Permuter(n, k, S):
    # writeyour code here
    return 0
Inputs = sys.argv[1].split("\n")
n, k = tuple(map(int, Inputs[0].split()))
S = list(map(int, Inputs[1].split()))
now = time.time()
output = Permuter(n, k, S)
then = time.time()
running_time = then - now
print("{}|{}".format(output, running_time))