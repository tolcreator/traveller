""" This script is for parsing .sec files """
""" There is no one solid definition for a .sec file. Probably the closest is
that given by the travellermap.com site:
    https://travellermap.com/doc/fileformats#sec
"""
from src.uwp.uwp import check_is_uwp_string_valid as uwp_check
import re



def parse_sec(sec: list[str]) -> list[dict]:
    """ This function parses the contents of a .sec file.
        The file would have been read with readlines and so we expect
        a list of strings, each string being a line from the file. """

    """ For now we will just return a list of systems. But in future
        we will want to parse out other info like sector / subsector
        names, size of the space, etc. """

    systems = []
    comments = []

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
            comments.append(line)
        else:
            try:
                systems.append(parse_system(line))
            except ValueError:
                pass

    """ Once we start parsing the details in the comments we can make this
        more sophisticated. In particular, the name of the space, and 
        possible subspaces i.e. subsectors, sectors """
    
    """ Find the first instance of 'Name: ' in the comments.
        This will be the name of the space. """
    name = "Unknown"
    for comment in comments:
        if "Name: " in comment:
            name = comment.replace("Name: ", "").strip()
            break

    contents = {
        "Name": name,
        "Systems": systems
            }
    return contents



def parse_system(line: str) -> dict:
    """ Try and parse the line as a system. If we get confused, raise an
        exception. This isn't the end of the world: chances are this is
        just a comment or something

        For now we will expect systems to be of the form:
           1 - x    : Name
        (x+1)-(x+4) : Hex Number
        (x+6)-(x+14): UWP
               x+17 : Bases
       (x+19)- y    : Codes and Comments
               y+2  : Zone
        (y+5)-(y+7) : PBG
        (y+9)-(y+10): Allegiance
       (y+12)+      : Stellar Data

        There are two variable length spaces. In the .sec files that come
        off travellermap.com, x = 14 and y = 47 (33-47 for codes and comments)
        This makes for very short names, and some trade codes can be longer
        than this space allows. So when we write .sec files, we will allow
        larger spaces. If we want to parse both, we will have to work it out.

        """
    system = {}

    """ We can identify where the name ends (and codes begins) by the well 
        formatted combination of coordinates, uwp, and bases """
    cub_search = \
            " [0-6][0-9][0-8][0-9] "\
            "[ABCDEX][0-9A][0-9A-Z][0-9A][0-9A][0-9A-Z][0-9A-Z]-[0-9A-Z]"\
            "  [ A-Z] "

    cubs = re.findall(cub_search, line)
    if len(cubs) != 1:
        """ This might not be a valid system """
        raise ValueError

    cub = cubs[0]
    name, remainder = re.split(cub_search, line)
    name = name.strip()
    remainder = remainder.strip()  

    system["Name"] = name
    system["Hex"] = cub[1:5]
    system["Uwp"] = cub[6:15]
    system["Bases"] = cub[17]

    """ We can identify where codes ends by the well formatted combindation
        of zone, PBG, and allegience. The remainder is the stellar data """

    zpa_search = " [ A-Z]  [0-9][0-9][0-9] [a-zA-Z][a-zA-Z] "
    zpas = re.findall(zpa_search, remainder)
    if len(zpas) != 1:
        """ If we got here this is some sort of error. """
        raise ValueError
    zpa = zpas[0]
    codes, stellar = re.split(zpa_search, remainder)
    codes = codes.strip()
    stellar = stellar.strip()

    system["Codes"] = codes
    system["Zone"] = zpa[1]
    system["Pbg"] = zpa[4:7]
    system["Allegiance"] = zpa[8:10]
    system["Stellar"] = stellar
    return system



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


