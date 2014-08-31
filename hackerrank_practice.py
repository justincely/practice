import sys
from itertools import combinations

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

    Parameters:
    -----------
    input_string, str
        appropriately formatted data string

    Returns:
    --------
    data : tuple
        total_byes (int), latency (int), bandwith (int), n_chunks (int),
        all_chunks (list of tuples)

    """

    all_lines = input_string.splitlines()

    total_bytes = int(all_lines[0])
    latency = int(all_lines[1])
    bandwidth = int(all_lines[2])
    n_chunks = int(all_lines[3])

    all_chunks = []
    for i, line in enumerate(all_lines[4:]):
        try:
            data = parse_line(line)
        except Exception as e:
            print 'line {} error: {}'.format(i, e)

        all_chunks.append(data)

    return total_bytes, latency, bandwidth, n_chunks, all_chunks

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
        recovered_bytes = recovered_bytes.union(set(range(start, stop)))
        
        if recovered_bytes == ref_bytes:
            return True

    return False

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

    total_bytes, latency, bandwidth, n_chunks, all_chunks = \
        parse_input(input_string)

    #-- Making sure it's possible
    if not byte_check(total_bytes, all_chunks):
        raise ValueError("The image cannot be recovered with too few bytes")

    #-- Computing times for each chunk
    times = {}
    for start, stop in all_chunks:
        times[(start, stop)] = read_time(stop - start, bandwidth, latency)

    #-- Computing Permutations
    permutations = []
    for i in xrange(1, len(all_chunks) + 1):
        permutations += list(combinations(all_chunks, i))

    #-- Finding the optimal value
    best_time = sum(times.values())
    best_combination = all_chunks

    for line in permutations:
        line_time = sum([times[item] for item in line])
        if byte_check(total_bytes, line) and line_time < best_time:
            best_time = line_time
            best_combination = line

    return best_time

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    print optimal_time(sys.stdin.read())
