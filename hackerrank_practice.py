import sys
from itertools import combinations
import heapq as hq

#-------------------------------------------------------------------------------

def uniform_cost_search(cost_data, nbytes):
    """Perform uniform cost search analysis on input collection of nodes.


    Parameters:
    -----------
    cost_data : dict
        dictionary of node, cost pairs
    nbytes : int
        number of bytes indicating success

    Returns:
    --------
    cost : float, None
        cost of the cheapest path, or None if no valid path found

    """

    explored = set()
    queue = []

    #start_node = hq.nsmallest(1, cost_data.keys())[0]
    #hq.heappush(queue, (cost_data[start_node], start_node, [start_node]))
    #-- Initialize queue at a zero-cost origin
    hq.heappush(queue, (0, (0, 1), [(0, 1)]) )

    while len(queue):
        cost, node, path = hq.heappop(queue)
        print 'At node:', node, cost, path

        #-- Exit on success condition of containing all needed bytes
        if byte_check(nbytes, path):
            print 'Best cost', cost, 'Best path', path
            return cost

        explored.add(node)

        for leaf in get_leafs(node, cost_data.iterkeys()):
            leaf_cost = cost + cost_data[leaf]

            if not leaf in explored:    
                queue_cost = [item[0] for item in queue]
                queue_nodes = [item[1] for item in queue]

                if not leaf in queue_nodes:
                    hq.heappush(queue, (leaf_cost, leaf, path + [leaf] ))

                elif (leaf in queue_nodes):
                    leaf_index = queue_nodes.index(leaf)
                    if leaf_cost < queue_cost[leaf_index]:
                        queue[leaf_index] = (leaf_cost, leaf, path + [leaf])
                        hq.heapify(queue)
                        
        
    return None

#-------------------------------------------------------------------------------

def generate_data(n_lines=100000):
    """Quick function to generate large random datasets for testing
    """

    import random
    nbytes = n_lines // 2

    with open('large_data.txt', 'w') as ofile:
        ofile.write('{}\n'.format(nbytes))
        ofile.write('15\n')
        ofile.write('10\n')
        ofile.write('{}\n'.format(n_lines))

        ofile.write('0,10\n')
        ofile.write('{},{}\n'.format(nbyes//2, nbytes))

        for i in xrange(n_lines):
            start = random.randint(0, nbytes-2)
            end = random.randint(start+1, nbytes-1)
            ofile.write('{},{}\n'.format(start, end))

#-------------------------------------------------------------------------------

def parse_line(line):
    """Check line formatting and parse data.

    Lines must be two integers separated by a comma.  Lines that do not meet the 
    criteria will raise an exception, lines which pass are returned as tuples of 
    ints.

    Parameters:
    -----------
    line : str
        line to be checked

    Returns: 
    --------
    data : tuple
        (start, stop) from input line

    Raises:
    -------
    ValueError if data not properly formatted

    """

    line = line.strip()

    if not line:
        raise ValueError("No data in line")
    if not ',' in line:
        raise ValueError("No comma in line")

    line = line.split(',')
    if not len(line) == 2:
        raise ValueError("Too many data values")

    try:
        data = (int(line[0]), int(line[1]))
    except:
        raise ValueError("Cannot convert line to ints")

    return data

#-------------------------------------------------------------------------------

def parse_input(input_string):
    """Split input data string into the various telemetry data

    According to given requirements:
    first line is the integer number of bytes in the original file.
    second line is the integer latency of the connection in seconds.
    third line is the bandwidth in bytes per second.
    fourth line is the number of data chunks.

    all remaining lines are the individual chunks of data.  Each line contains
    the comma separated starting and ending indices of the data chunk in bytes.

    basic data formatting checks will be done. Errors will be raised for badly
    formatted lines but processing will attempt to continue with the valid data.

    Parameters:
    -----------
    input_string, str
        appropriately formatted data string

    Returns:
    --------
    data : tuple
        total_bytes (int), all_chunks (list of tuples)

    """

    all_lines = input_string.splitlines()

    total_bytes = int(all_lines[0])
    latency = int(all_lines[1])
    bandwidth = int(all_lines[2])
    n_chunks = int(all_lines[3])

    all_chunks = {}
    for i, line in enumerate(all_lines[4:]):
        try:
            data = parse_line(line)
        except Exception as e:
            print 'line {} error: {}'.format(i, e)

        all_chunks[data] = read_time(data[1] - data[0], bandwidth, latency)

    return total_bytes, all_chunks

#-------------------------------------------------------------------------------

def read_time(size, bandwidth, latency):
    """Calculate the time to link and read a chunk of data.

    Parameters:
    -----------
    size : float, int
        Total size of the data chunk in bytes
    bandwidth : float, int
        Bandiwidth of the connection in bytes per second.
    latency : float, int
        Latency of the connection in seconds.

    Returns:
    --------
    total_time : float
        time to downlink in seconds.

    """

    return 2.0 * latency + (float(size) / bandwidth)

#-------------------------------------------------------------------------------

def byte_check(ref_bytes, chunks):
    """Check to see if the image recovery is possible.

    Assemble set of input bytes from each chunk until the recovered set matches
    that in the reference bytes.  The first instance of the two sets matching
    will cause a return with True.  The sets not matching after all chunks 
    have been parsed will return False.

    Parameters:
    -----------
    ref_bytes : int, iterable
        bytes in the original data.  if int, bytes will assume to start from 0.
        if iterable, conversion to set will be attempted.
    chunks : list of tuples
        list of (start, stop) bytes as output by parse_input

    Returns:
    --------
    recovery_possible : bool
       Whether or not the data can be recovered

    """
 
    recovered_bytes = set()

    if isinstance(ref_bytes, int):
        ref_bytes = set(range(ref_bytes))
    elif isinstance(ref_bytes, (list, tuple, str)):
        ref_bytes = set(ref_bytes)
    elif isinstance(ref_bytes, set):
        pass
    else:
        raise ValueError("ref_bytes must be able to become a set")

    for start, stop in chunks:
        recovered_bytes = recovered_bytes.union(set(xrange(start, stop)))

        if ref_bytes.issubset(recovered_bytes):
            return True

    return False

#-------------------------------------------------------------------------------

def get_leafs(start_node, all_nodes):
    """Find leaf nodes from the given starting node.


    Parameters:
    -----------
    start_node : tuple
        node from which to find leaves
    all_nodes: list
        list of all available nodes

    Returns:
    --------
    node_iterator : generator expression
        iterable generator of available leaf nodes

    """

    return (node for node in all_nodes if (node != start_node and
                                           node[0] >= start_node[0] and
                                           node[0] <= start_node[1] and 
                                           node[1] >= start_node[1]))

#-------------------------------------------------------------------------------

def generate_graph(data_dict, prune=False):
    """Create graph from input data

    Parameters:
    -----------
    data_dict : dict
        dict of nodes
    prune : bool, optional
        remove nodes with no leafs

    Returns:
    --------
    graph : dict
        node, leaf-list dictionary
    
    """

    graph = data_dict.copy()
    all_nodes = graph.keys()

    for i, node in enumerate(all_nodes):

        leafs = get_leafs(node, all_nodes)
        graph[node] = leafs

        print i, len(all_nodes)

        if prune and not len(leafs):
            del graph[node]

    return graph

#-------------------------------------------------------------------------------

def generate_permutations(all_chunks):
    """Create list of all possible combination of input iterable.

    """

    for i in xrange(1, len(all_chunks) + 1):
        for permutation in combinations(all_chunks, i):
            yield list(permutation)

#-------------------------------------------------------------------------------

def optimal_time(input_string):
    """Find the best-case downlink time from the available data-chunks.

    Assumed formatting of input_string:
    first line is the integer number of bytes in the original file.
    second line is the integer latency of the connection in seconds.
    third line is the bandwidth in bytes per second.
    fourth line is the number of data chunks.

    all remaining lines are the individual chunks of data.  Each line contains
    the comma separated starting and ending indices of the data chunk in bytes.


    Parameters:
    -----------
    input_string, str
        string containing the formatted input data

    Returns:
    --------
    best_time : float
        the smallest amount of time to read the data for the entire image

    """

    total_bytes, data = parse_input(input_string)

    best_time = uniform_cost_search(data, total_bytes)

    if best_time:
        return round(best_time, 3)

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    print optimal_time(sys.stdin.read())
