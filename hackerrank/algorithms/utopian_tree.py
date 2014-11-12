"""Compute utopian tree for hackerrank
"""

import sys

def growth(initial=1, cycles=1):
    """Compute growth for the utopian tree
    """

    for i in xrange(cycles):
        if not i % 2:
            initial *= 2
        if i % 2:
            initial += 1

    return initial

if __name__ == "__main__":
    buffer = [line for line in sys.stdin.readlines()]
    N_cases = int(buffer[0].strip())

    for val in buffer[1:N_cases+1]:
        val = int(val.strip())
        print growth(1, cycles=val)
