import sys

#-------------------------------------------------------------------------------

def compute_permutations(total_cents, available_coins):
    """Permute the available coins to sum to the total

    Parameters
    ----------
    total_cents : int
        value to sum to
    available_coins : list
        list of coin denominations available

    Returns
    -------
    n_permutations : int
        number of ways to make the total

    """

    useful_coins = [coin for coin in available_coins if coin <= total_cents]

    combinations = [1] + [0] * total_cents
    for coin in useful_coins:
        for i in xrange(coin, total_cents+1):
            combinations[i] += combinations[i - coin]
            print coin, i, combinations

    return combinations[-1]

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    cents = None
    coins = None

    for i, line in enumerate(sys.stdin.readlines()):
        if i == 0:
            cents = int(line.strip())
        if i == 1:
            coins = map(int, line.strip().split())

    if (cents == None) or (coins == None):
        raise IOError('Failed to parse input values')

    print compute_permutations(cents, coins)
