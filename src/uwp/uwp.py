""" Script for dealing with UWPs """

import src.utils.ehex as ehex
from src.utils.ehex import Ehex

def check_is_uwp_string_valid(uwp_string):
    """ Checks if this is a well formed uwp_string with sane values

        A valid UWP is of the form S123456-7 where
        S indicates Starport and can be A,B,C,D,E or X
        1 through 7 are 'hex' values and must be on the hex table
        - separates tech level from the rest of the string and must
        be present. """

    if len(uwp_string) != 9:
        print(f"uwp_string '{uwp_string}' incorrect length:" \
                f"{len(uwp_string)}")
        return False

    if uwp_string[-2] != '-':
        print(f"uwp_string '{uwp_string}' second last character" \
                f"is not '-': '{uwp_string[-2]}'")
        return False

    if uwp_string[0] not in ['A', 'B', 'C', 'D', 'E', 'X']:
        print(f"uwp_string '{uwp_string}' invalid starport: {uwp_string[0]}")
        return False

    hexvalues = uwp_string[1:-2] + uwp_string[-1]

    for hexvalue in hexvalues:
        if not ehex.is_valid(hexvalue):
            print(f"In uwp_string '{uwp_string}' Found character that is" \
                    f" not a hex value: '{hexvalue}'")
            return False

    return True

class Uwp:

    """ TODO I'd also like to be able to create a Uwp from a list
        (maybe a tuple) of Ehexes. """
    def __init__(self, uwp_string):
        """ Creates the world from a given UWP string """

        if not check_is_uwp_string_valid(uwp_string):
            raise ValueError

        self.starport = Ehex(uwp_string[0])
        self.size = Ehex(uwp_string[1])
        self.atmosphere = Ehex(uwp_string[2])
        self.hydrosphere = Ehex(uwp_string[3])
        self.population = Ehex(uwp_string[4])
        self.government = Ehex(uwp_string[5])
        self.law_level = Ehex(uwp_string[6])
        self.tech_level = Ehex(uwp_string[8])

    def __str__(self):
        return str(self.starport) + \
                str(self.size) + \
                str(self.atmosphere) + \
                str(self.hydrosphere) + \
                str(self.population) + \
                str(self.government) + \
                str(self.law_level) + "-" +\
                str(self.tech_level)

if __name__ == "__main__":
    w = Uwp("D867A77-8")
    print(w)

