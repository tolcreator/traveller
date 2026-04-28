""" Script for dealing with UWPs """

import src.utils.ehex as ehex
from src.utils.ehex import Ehex

def check_is_uwp_string_valid(uwp_string: str) -> bool:
    """ Checks if this is a well formed uwp_string with sane values

        A valid UWP is of the form S123456-7 where
        S indicates Starport and can be A,B,C,D,E or X
        1 through 7 are 'hex' values and must be on the hex table
        - separates tech level from the rest of the string and must
        be present. """

    if not isinstance(uwp_string, str):
        return False

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

def check_is_uwp_tuple_valid(uwp_tuple: tuple) -> bool:
    """ Checks if this is a tuple of ehexes of the correct length
        and with sane values """

    if not isinstance(uwp_tuple, tuple):
        return False

    if len(uwp_tuple) != 8:
        return False

    for candidate in uwp_tuple:
        if not isinstance(candidate, Ehex):
            return False

    if uwp_tuple[0] not in ['A', 'B', 'C', 'D', 'E', 'X']:
        """ First element must be starport and must have one of
            these values """
        return False

    return True

def check_is_uwp_dict_valid(uwp_dict: dict) -> bool:
    """ Checks if this is a dict with the correct fields """
    if not isinstance(uwp_dict, dict):
        return False

    expected_fields = [
            "Starport",
            "Size",
            "Atmosphere",
            "Hydrosphere",
            "Population",
            "Government",
            "Law Level",
            "Tech Level"]

    for expected_field in expected_fields:
        if expected_field not in uwp_dict:
            return False
        if not isinstance(uwp_dict[expected_field], Ehex):
            return False

    if uwp_dict["Starport"] not in ['A', 'B', 'C', 'D', 'E', 'X']:
        """ Starports have a restricted possibility of values """
        return False

    return True

class Uwp:
    def __init__(self, source: str | tuple | dict):
        """ Creates the world from a given UWP string """

        if isinstance(source, str):
            if not check_is_uwp_string_valid(source):
               raise ValueError

            self.starport = Ehex(source[0])
            self.size = Ehex(source[1])
            self.atmosphere = Ehex(source[2])
            self.hydrosphere = Ehex(source[3])
            self.population = Ehex(source[4])
            self.government = Ehex(source[5])
            self.law_level = Ehex(source[6])
            self.tech_level = Ehex(source[8])

        elif isinstance(source, tuple):
            if not check_is_uwp_tuple_valid(source):
                raise ValueError

            self.starport = source[0]
            self.size = source[1]
            self.atmosphere = source[2]
            self.hydrosphere = source[3]
            self.population = source[4]
            self.government = source[5]
            self.law_level = source[6]
            self.tech_level = source[7]

        elif isinstance(source, dict):
            if not check_is_uwp_dict_valid(source):
                raise ValueError

            self.starport = source["Starport"]
            self.size = source["Size"]
            self.atmosphere = source["Atmosphere"]
            self.hydrosphere = source["Hydrosphere"]
            self.population = source["Population"]
            self.government = source["Government"]
            self.law_level = source["Law Level"]
            self.tech_level = source["Tech Level"]

        else:
            raise TypeError


    def __str__(self) -> str:
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

