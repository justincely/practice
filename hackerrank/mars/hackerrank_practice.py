import sys
import heapq as hq

#-------------------------------------------------------------------------------

def byte_check(ref_bytes, chunks):
    """Check to see if the image recovery is possible.

    chunks is assumed to be an iterable of (start, stop) byte pairs that
    are contigous accross their range.  The check is performed to assert 
    that there is contigous covrage of bytes from 0 to ref_bytes.

    Parameters:
    -----------
    ref_bytes : int
        bytes in the original data.
    chunks : list of tuples
        list of (start, stop) bytes as output by parse_input

    Returns:
    --------
    recovery_possible : bool
       Whether or not the data can be recovered

    """

    if not len(chunks):
        return False

    chunks = sorted(chunks)

    byte_min, byte_max = chunks[0]

    for start, stop in chunks[1:]:
        if (start >= byte_min) and (start <= byte_max) and (stop > byte_max):
            byte_max = stop

    if (byte_min, byte_max) == (0, ref_bytes):
        return True
    else:
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

    if not byte_check(total_bytes, data):
        return None

    best_time = uniform_cost_search(data, total_bytes)

    return best_time

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

def parse_line(line):
    """Check line formatting and parse data.

    Lines must be two integers separated by a comma.  Lines that do not meet 
    the criteria will raise an exception, lines which pass are returned as 
    tuples of ints.

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

    #-- Initialize queue at a zero-cost origin
    hq.heappush(queue, (0, (0, 1), [(0, 1)]) )

    while len(queue):
        cost, node, path = hq.heappop(queue)

        #-- Exit on success condition of containing all needed bytes
        if byte_check(nbytes, path):
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

def test_byte_check_pass():
    """Check cases for which the byte_check function should pass
    """

    overlapping = [(0, 20), (10, 20), (5, 40)]
    assert byte_check(40, overlapping), "Didn't work with overlapping values"

    single = [(0, 20)]
    assert byte_check(20, single), "Didn't work with single chunk"

    edges = [(0, 20), (20, 40), (40, 100)]
    assert byte_check(100, edges), "Didn't work with just touching edges"

    copies = [(0, 20), (20, 40), (40, 100), (40, 100)]
    assert byte_check(100, copies), "Didn't work with copies"

#-------------------------------------------------------------------------------

def test_byte_check_fail():
    """Check cases for which the byte check function should fail
    """

    gap = [(0, 20), (21, 40), (40, 80)]
    assert not byte_check(80, gap), "Didn't fail with single value gapped data"

    gap.append((100, 200))
    assert not byte_check(80, gap), "Didn't fail with large gap"

    wrong_range = [(0, 20), (40, 80), (80, 100)]
    assert not byte_check(80, wrong_range), "Didn't fail with wrong range"

    assert not byte_check(80, []), "Didn't fail with empty chunks"

    assert not byte_check(80, [(1, 20), (20, 80)]), "Didn't fail with missing 0"

#-------------------------------------------------------------------------------

def test_parsing():
    """Test string parsing functions
    """
    from nose.tools import assert_raises

    assert parse_line('500,600') == (500,600), 'Failed on OK string'
    assert parse_line('500, 600') == (500,600), 'Failed on OK string'
    assert_raises(ValueError, parse_line, '500,600,700')
    assert_raises(ValueError, parse_line, '500600')
    assert_raises(ValueError, parse_line, '')
    assert_raises(ValueError, parse_line, '500,six')


    #--Check input parsing from mangled input
    input_string = '2000\n'
    input_string += '15\n'
    input_string += '10\n'
    input_string += '7\n'
    input_string += '0,200\n'
    input_string += '200,400\n'
    input_string += '400,600,1000\n'
    input_string += '600,800\n'
    input_string += '800,1000\n'
    input_string += '\n'
    input_string += '1000,2000\n'
    input_string += 'adfsa\n'
    input_string += '0,1800\n'

    assert parse_input(input_string) == (2000,  {(0, 200): 50.0,
                                                 (0, 1800): 210.0,
                                                 (200, 400): 50.0,
                                                 (600, 800): 50.0,
                                                 (800, 1000): 50.0,
                                                 (1000, 2000): 130.0})

#-------------------------------------------------------------------------------

def test_leafs():
    """Test the leaf-finding logic
    """

    node = (0, 5)
    all_nodes = [(20, 40), (30, 40), (0, 10), (0, 40), (0, 2)]
    assert set(get_leafs(node, all_nodes)) == set([(0, 10), (0, 40)]), \
        "Failed to find leafs from same-start cases"

    node = (10, 25)
    assert set(get_leafs(node, all_nodes)) == set([(20, 40)]), \
        "Failed to find leafs from intersecting case"

    node = (10, 19)
    assert set(get_leafs(node, all_nodes)) == set(), \
        "Failed to find 0 leafs from full set of nodes."

    assert set(get_leafs((0, 1), [])) == set(), \
        "Failed to find 0 leafs from empty set of nodes."

#-------------------------------------------------------------------------------

def test_given_cases():
    """Check the two input/output cases supplied in the instructions
    """

    assert optimal_time(open('input000.txt').read()) == \
        float(open('output000.txt').read()), "test-case 0 failed"
    
    assert optimal_time(open('input001.txt').read()) == \
        float(open('output001.txt').read()), "test-case 1 failed"

#-------------------------------------------------------------------------------

def test_read_time():
    """Check basic math of the read_time function
    """

    assert read_time(10, 10, 10) == 21, "Incorrect calculation with ints"
    assert read_time(10.0, 10.0, 10.0) == 21, "Incorrect calculation of floats"
    assert read_time(5, 2, 1) == 4.5, "Int division not handled"

#-------------------------------------------------------------------------------

def test_ucs():
    """Test that the uniform cost search algorithm correctly finds the shortest
    path or returns None
    """
    
    nbytes = 2000
    cost_data = {(0, 200):5,
                 (200, 400):5,
                 (400, 600):5,
                 (600, 800):5,
                 (800, 1000):5,
                 (0, 2000):3,
                 (1000, 2000):5}

    #-- Known shortest path of single chunk
    assert uniform_cost_search(cost_data, nbytes) == 3, \
        'Failed to find shortest path of 1 chunk'

    #-- New shortest path of two chunks
    cost_data[(0, 500)] = 1
    cost_data[(500, 2000)] = 1
    assert uniform_cost_search(cost_data, nbytes) == 2, \
        'Failed with two chunk path'

    #-- Single chunk
    cost_data = {(0, 2000):5}
    assert uniform_cost_search(cost_data, nbytes) == 5, \
        'Failed to find shortest path from only 1 chunk'

    #-- No valid path through
    cost_data = {(1, 200):5,
                 (500, 700):10}
    assert uniform_cost_search(cost_data, nbytes) == None, \
        'Failed to return None with no valid path'

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    best_time = optimal_time(sys.stdin.read())
    
    if best_time:
        print "{0:.3f}".format(best_time)
    
