import sys

#-------------------------------------------------------------------------------

def factorial(N):
    """Compute factorial of input value.

    Needed as neither numpy nor scipy libraries are available

    Paramters
    ---------
    N : int
        value for which to calculate the factorial

    Returns
    -------
    total : int
        computed factorial

    """

    total = 1
    for val in xrange(N, 0, -1):
        total *= val
    return total

#-------------------------------------------------------------------------------

def n_ways(flips, heads):
    """Compute possible ways to flip given number of heads.

    Parameters
    ----------
    flips : int
        number of total flips
    heads : int
        number heads desired

    """
    
    if heads > flips:
        raise ValueError('N heads cannot be higher than M flips')

    tails = flips - heads

    return int(factorial(flips) / (factorial(heads) * factorial(tails)))

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    (m_flips, n_heads) = map(int, sys.stdin.read().strip().split())

    print n_ways(m_flips, n_heads)
