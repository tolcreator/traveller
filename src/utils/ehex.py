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
hex_table = (
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
    )

class Ehex:
    def __init__(self, value: str = '0'):
        """ No need to do any checks here. The assignment will call
            our custom __setattr__ method below, which will perform
            any necessary checks. """
        self.value = value

    def __setattr__(self, attribute: str, value: int | str):
        """ value here can be an int from 0 to 35
            or a character which appears in hex_table """
        if isinstance(value, int):
            if value >= 0 and value < len(hex_table):
                object.__setattr__(self, attribute, hex_table[value])
            else:
                raise ValueError
        elif isinstance(value, str):
            if value in hex_table:
                object.__setattr__(self, attribute, value)
            else:
                raise ValueError("Ehex must be between 0('0') and 35('Z')")
        else:
            raise TypeError

    def __int__(self) -> int:
        return hex_table.index(self.value)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: int | str | Ehex) -> bool:
        """ We can compare an Ehex with an int, a str, or another
            ehex. A nonsensical comparison: with another object,
            or with something out of bounds, can just be False:
            no need to raise an exception. """
        if isinstance(other, int):
            if other >= 0 and other < len(hex_table):
                return self.value == hex_table[other]
            else:
                return False
        elif isinstance(other, str):
            return self.value == other
        elif isinstance(other, Ehex):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other: int | str | Ehex) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: int | str | Ehex) -> bool:
        """ Less Than """
        if isinstance(other, int):
            return self.value < int_to_hex(other)
        elif isinstance(other, str):
            if other in hex_table:
                return self.value < other
            else:
                raise ValueError("Ehex must be between 0('0') and 35('Z')")
        elif isinstance(other, Ehex):
            return self.value < other.value
        else:
            raise TypeError

    def __le__(self, other: int | str | Ehex) -> bool:
        """ Less Than or Equal To """
        if isinstance(other, int):
            return self.value <= int_to_hex(other)
        elif isinstance(other, str):
            if other in hex_table:
                return self.value <= other
            else:
                raise ValueError("Ehex must be between 0('0') and 35('Z')")
        elif isinstance(other, Ehex):
            return self.value <= other.value
        else:
            raise TypeError

    def __gt__(self, other: int | str | Ehex) -> bool:
        """ Greater Than """
        if isinstance(other, int):
            return self.value > int_to_hex(other)
        elif isinstance(other, str):
            if other in hex_table:
                return self.value > other
            else:
                raise ValueError("Ehex must be between 0('0') and 35('Z')")
        elif isinstance(other, Ehex):
            return self.value > other.value
        else:
            raise TypeError

    def __ge__(self, other: int | str | Ehex) -> bool:
        """ Greater Than or Equal To"""
        if isinstance(other, int):
            return self.value >= int_to_hex(other)
        elif isinstance(other, str):
            if other in hex_table:
                return self.value >= other
            else:
                raise ValueError("Ehex must be between 0('0') and 35('Z')")
        elif isinstance(other, Ehex):
            return self.value >= other.value
        else:
            raise TypeError



def hex_to_int(hex_value: str) -> int:
    """ Converts a string 'hex' value into an int. """
    if isinstance(hex_value, str):
        if hex_value in hex_table:
            return hex_table.index(hex_value)
        else:
            raise ValueError("Ehex must be between 0('0') and 35('Z')")
    else:
        raise TypeError

def int_to_hex(value: int) -> str:
    """ Converts an int value into a string 'hex' value """
    if isinstance(value, int):
        if value >= 0 and value < len(hex_table):
            return hex_table[value]
        else:
            raise ValueError("Ehex must be between 0('0') and 35('Z')")
    else:
        raise TypeError

def is_valid(a: str) -> bool:
    if a in hex_table:
        return True
    return False
