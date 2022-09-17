import math
import random
import time
import sys

def MotDePasse(N, K):
    p = 1
    for i in range(K-N+1, K+1):
        p *= i
    return p%(10**9+7)
N, K = tuple(map(int, sys.argv[1].split()))
now = time.time()
output = MotDePasse(N, K)
then = time.time()
running_time = then-now
print("{}|{}".format(output, running_time))