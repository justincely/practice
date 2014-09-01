import sys
from itertools import combinations
from collections import deque
import heapq as hq

#-------------------------------------------------------------------------------

def uniform_cost_search(g, cost_data, nbytes):
    explored = set()
    queue = []

    #node = hq.nsmallest(1, g.keys())[0]
    #hq.heappush(queue, (node, cost_data[node]) )
    hq.heappush(queue, ((0, 1), 0, []) )
    g[(0, 1)] = [key for key in g.keys() if key[0] == 0]

    while len(queue):
        node, cost, path = hq.heappop(queue)

        if byte_check(nbytes, path):
            print 'Best cost', cost, 'Best path', path
            return cost

        explored.add(node)

        for leaf in g[node]:
            leaf_cost = cost + cost_data[leaf]

            if not leaf in explored:
                queue_nodes = [item[0] for item in queue]
                queue_cost = [item[1] for item in queue]

                if not leaf in queue_nodes:
                    hq.heappush(queue, (leaf, leaf_cost, path + [leaf] ))

                elif (leaf in queue_nodes) and leaf_cost < queue_cost[queue_nodes.index(leaf)]:
                        node = leaf
                        cost = leaf_cost
                        hq.heappush(queue, (leaf, leaf_cost, path + [leaf] ))
        
    return None

#-------------------------------------------------------------------------------

def generate_data(n_lines=100000):
    import random
    nbytes = n_lines * 2

    with open('large_data.txt', 'w') as ofile:
        ofile.write('{}\n'.format(nbytes))
        ofile.write('15\n')
        ofile.write('10\n')
        ofile.write('{}\n'.format(n_lines))

        for i in xrange(n_lines):
            start = random.randint(0, nbytes-2)
            end = random.randint(start+1, nbytes-1)
            ofile.write('{},{}\n'.format(start, end))

#-------------------------------------------------------------------------------

def parse_line(line):
    """Check line formatting and parse data.

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
    """Split input data string into the various telemetry data according 
    to given formatting guidelines.

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
    ### Try generator next
    ### check boundary cases
    return [node for node in all_nodes if (node != start_node and
                                           node[0] >= start_node[0] and
                                           node[0] <= start_node[1] and 
                                           node[1] >= start_node[1])]

#-------------------------------------------------------------------------------

def generate_graph(data_dict):
    graph = data_dict.copy()
    all_nodes = graph.keys()

    for i, node in enumerate(all_nodes):

        leafs = get_leafs(node, all_nodes)
        graph[node] = leafs

        print i, len(all_nodes)

        #if not len(leafs):
        #    del graph[node]

    return graph

#-------------------------------------------------------------------------------

def generate_permutations(all_chunks):
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

    #print "#-- Checking bytes"
    #if not byte_check(total_bytes, data.keys()):
    #    #raise ValueError("The image cannot be recovered with too few bytes")
    #    return

    print "#-- Generating graph"
    graph = generate_graph(data)
    print graph

    best_time = uniform_cost_search(graph, data, total_bytes)

    print best_time
    return round(best_time, 3)

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    print optimal_time(sys.stdin.read())
