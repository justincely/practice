""" Practice

"""

import numpy as np
import functions

#-------------------------------------------------------------------------------

def problem_1(N=1000):
    """ If we list all the natural numbers below 10 that are multiples of 
    3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

    Find the sum of all the multiples of 3 or 5 below 1000.

    """

    natural_numbers = np.arange(N)

    index = np.where( np.logical_not(natural_numbers % 3) | 
                      np.logical_not(natural_numbers % 5) )

    return natural_numbers[index].sum()

#-------------------------------------------------------------------------------

def problem_2(limit=4e6):
    """ Each new term in the Fibonacci sequence is generated by adding the 
    previous two terms. By starting with 1 and 2, the first 10 terms will be:

    1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

    By considering the terms in the Fibonacci sequence whose values do not 
    exceed four million, find the sum of the even-valued terms.

    """

    # This could be made much faster
    
    sum = 0
    iteration = 0
    current = functions.fibonacci(iteration)
    
    while current < limit:

        if not current % 2:
            sum += current

        iteration += 1
        current = functions.fibonacci(iteration)
        
    return sum

#-------------------------------------------------------------------------------

def problem_3(N=600851475143):
    """ prime factors of 13195 are 5, 7, 13 and 29.

    What is the largest prime factor of the number 600851475143 ?

    """

    all_factors = list(functions.factors(N))
    
    max_prime = 1
    for factor in all_factors:
        if factor > max_prime and functions.isprime(factor):
            max_prime = factor

    return max_prime

#-------------------------------------------------------------------------------

def problem_4():
    """A palindromic number reads the same both ways. The largest palindrome
    made from the product of two 2-digit numbers is 9009 = 91 x 99.

    Find the largest palindrome made from the product of two 3-digit numbers.
    
    """

    largest = 0

    for val1 in xrange(100, 1000):
        for val2 in xrange(100, 1000):
            prod = val1 * val2
            if (str(prod) == str(prod)[::-1]) and (prod > largest):
                largest = prod

    return largest
    
#-------------------------------------------------------------------------------

def problem_5(N=20):
    """2520 is the smallest number that can be divided by each of the numbers 
    from 1 to 10 without any remainder.

    What is the smallest positive number that is evenly divisible by all 
    of the numbers from 1 to 20?

    """
    
    out = N
    leave = False

    while not leave:
        out += N
        leave = True

        for val in xrange(N, 1, -1):
            if out % val:
                leave = False
                break

    return out

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    print "Problem 1: ", problem_1()
    print "Problem 2: ", problem_2()
    print "Problem 3: ", problem_3()
    print "Problem 4: ", problem_4()
    print "Problem 5: ", problem_5()
