""" Traveller 'ehex' values 
    A case could be made for a very minimal approach here. I could
    just have:
        The hex table
        a hex to int method
        a int to hex method
        an is valid method
    and leave it at that. What's neat is that comparisons between
    the string values on the hex table are all valid: that is 
        '0' < '2', '4' < 'A', and 'B' < 'F' are all true.

    Alternatively I could have a class Ehex which overrides various
    dunder methods so that it acts... nicely. You can compare ehexes,
    compare ehexes to strings (that appear on the hex table), and
    compare ehexes to numbers (that are in bounds). It could check
    that values are in bounds on assignment. This is all very "extra"
    but the value is probably mainly in the exercise here.

"""

# So called "hex" values can actually be larger than 'F'
hex_table = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

def hex_to_int(hex_value):
    """ Converts a string 'hex' value into an int. """
    if isinstance(hex_value, str):
        if hex_value in hex_table:
            return hex_table.index(hex_value)
        else:
            raise ValueError
    else:
        raise TypeError

def int_to_hex(value):
    """ Converts an int value into a string 'hex' value """
    if isinstance(value, int):
        if value < len(hex_table):
            return hex_table[value]
        else:
            raise ValueError
    else:
        raise TypeError

def is_valid(a):
    if a in hex_table:
        return True
    return False
