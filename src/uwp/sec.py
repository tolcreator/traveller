""" This script is for parsing .sec files """
""" There is no one solid definition for a .sec file. Probably the closest is
that given by the travellermap.com site:
    https://travellermap.com/doc/fileformats#sec
"""
from src.uwp.uwp import check_is_uwp_string_valid as uwp_check



def parse_sec(sec: list[str]) -> list[dict]:
    """ This function parses the contents of a .sec file.
        The file would have been read with readlines and so we expect
        a list of strings, each string being a line from the file. """

    """ For now we will just return a list of systems. But in future
        we will want to parse out other info like sector / subsector
        names, size of the space, etc. """

    systems = []

    for line in sec:
        line = line.strip()
        if len(line) == 0:
            pass
        elif line[0] == '#':
            """ This is a comment, we can ignore it... FOR NOW """
            """ This can contain information like sector name,
                subsector names, allegiance codes, etc. Eventually
                we DO want to parse these things. """
            line = line[1:]
            line = line.strip()
        else:
            try:
                systems.append(parse_system(line))
            except ValueError:
                pass

    """ Once we start parsing the details in the comments we can make this
        more sophisticated. In particular, the name of the space, and 
        possible subspaces i.e. subsectors, sectors """
    contents = {
        "Systems": systems
            }
    return contents



def parse_system(line: str) -> dict:
    """ Try and parse the line as a system. If we get confused, raise an
        exception. This isn't the end of the world: chances are this is
        just a comment or something

        For now we will expect systems to be of the form:
         1-14: Name
        15-18: Hex Number
        20-28: UWP
           31: Bases
        33-47: Codes and Comments
           49: Zone
        52-54: PBG
        56-57: Allegiance
        59-74: Stellar Data

        """
    system = {}
    system["Name"] = line[:14].strip()
    system["Hex"] = line[14:18].strip()
    system["Uwp"] = line[19:28].strip()
    system["Bases"] = line[30:31].strip()
    system["Codes"] = line[32:47].strip()
    system["Zone"] = line[48:49].strip()
    system["Pbg"] = line[51:54].strip()
    system["Allegiance"] = line[55:57].strip()
    system["Stellar"] = line[58:].strip()
    """ Sanity check values. Does this look like a system? """
    if system["Hex"].isnumeric() and uwp_check(system["Uwp"]):
        return system
    else:
        raise ValueError



if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as fp:
                sec = fp.readlines()
        except IOError:
            print(f"Could not read file '{filename}'")
        parse_sec(sec)
    else:
        print("I expect to be given a file name to read")


