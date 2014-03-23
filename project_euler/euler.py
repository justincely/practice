""" Practice

"""

import numpy as np

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

if __name__ == "__main__":
    print problem_1()
