import sys

#-------------------------------------------------------------------------------

def clean(input_line):
    """Strip line of symbols and convert to lower-case

    Parameters
    ----------
    input_line : str
        single line of text

    Returns
    -------
    output_line : str
        cleaned single line

    """

    output_line = ''

    for item in input_line:
        if item.isalnum():
            output_line += item.lower()
        elif item.isspace():
            output_line += item
        else:
            pass

    return output_line

#-------------------------------------------------------------------------------

def assemble_anagrams(words):
    """Create a dictionary of anagrams

    Parameters
    ----------
    words : list
        words to parse for possible anagrams

    Returns
    -------
    anagrams : dict
        anagrams matched to their frozenset of characters

    """

    anagrams = {}
    checked = set()

    for item in words:
        if item in checked:
            continue

        characters = frozenset(item)
        if not characters in anagrams:
            anagrams[characters] = [item]
        else:
            anagrams[characters].append(item)

        checked.add(item)

    return anagrams

#-------------------------------------------------------------------------------

if __name__ == "__main__":
     input_line = sys.stdin.read().strip()
     words = clean(input_line).split()

     anagram_counts = assemble_anagrams(words)

     outputs = [sorted(item) for item in anagram_counts.itervalues() if len(item) > 1]

     for item in sorted(outputs):
         print ' '.join(sorted(item))
