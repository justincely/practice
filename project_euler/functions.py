""" Quick needed mathematical functions

"""
import numpy as np

#-------------------------------------------------------------------------------

def fibonacci(n):
    if n == 0: 
        return 0
    elif n == 1: 
        return 1
    else: 
        return fibonacci(n-1) + fibonacci(n-2)

#-------------------------------------------------------------------------------

def isprime(number):
    if number == 2:
        return True
    if number < 2 or not number % 2:
        return False
    
    for value in xrange(3, int(np.sqrt(number))+1, 2):
        if not number % value:
            return False

    return True

#-------------------------------------------------------------------------------

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

#-------------------------------------------------------------------------------

def collatz(start):
    if not start > 0:
        raise ValueError('input value must be larger than 1')

    sequence = []
    sequence.append(start)
    
    while start != 1:
        if not start % 2:
            start /= 2
        else:
            start = (3 * start) + 1
        
        sequence.append(start)

    return sequence

#-------------------------------------------------------------------------------
