"""
Suppose that we are given a very long list of strings.  We know that some of the strings are encrypted copies of other strings in the list, but we don't know which.  We do know that any encrypted string was encrypted using a simple substitution cipher (i.e. "A maps to B, C maps to D, etc.")
 
So given the long list of strings, we want to know the NUMBER OF PAIRS of strings that could potentially be encrypted copies of each other.  That is, 'ABCA' and 'XYZX' match because there exists a substitution cipher that transforms one to the other (and an inverse map for transforming it back).  However, 'ABCA' and 'ABCD' are not matches because no such substitution cipher exists.

match: there exists sub. cipher C s.t. C(s_1) = s_2, C^-1(s_2) = s_1

ABCA -> XYZX

>>> get_num_cipher_matches(['ABCA', 'XYZX', 'QWEQ', 'BEER', 'FOOBAR', 'ABBCDE'])
4
 
List of cipher-matches:
[('ABCA', 'XYZX'), ('ABCA', 'QWEQ'), ('QWEQ', 'XYZX'), ('FOOBAR', 'ABBCDE')]
"""

from itertools import combinations

def get_num_cipher_matches(input_list):
    """Determine the number of possible cypher matches
    
    Parameters:
    -----------
    input_list : list
        list of strings to check
    
    Returns:
    --------
    num_matches : int
        number of string matches found
        
    """
    
    if isinstance(input_list, str):
        return 0
    
    count = 0
    for raw_string, cypher_string in combinations(input_list, 2):
        if is_match(raw_string, cypher_string):
            count += 1
                
    return count


def is_match(raw_string, cypher_string): 
    """Check to see if raw_string could be a 
    unencrypted verison of cypher_string
    
    Parameters:
    -----------
    raw_string : str
        un-encrypted string
    cypher_string : str
        potential encrypted string to match against
        
    Returns:
    --------
    match_found : bool
        whether the strings could be permutations
        
    """
    
    if not len(raw_string) == len(cypher_string):
        return False
    
    pairs = {}
    
    for raw_char, cypher_char in zip(raw_string, cypher_string):
        
        if cypher_char in pairs and pairs[cypher_char] != raw_char:
            return False
        elif not raw_char in pairs:
            pairs[raw_char] = cypher_char
        elif raw_char in pairs and pairs[raw_char] != cypher_char:
            return False
        else:
            pass
        
    return True

print is_match('ABCA', 'XYZX')
print is_match('ABCA', 'ABCD') 
print is_match('ABCD', 'ABCA')
print get_num_cipher_matches(['ABCA', 'XYZX', 'QWEQ', 'BEER', 'FOOBAR', 'ABBCDE'])
