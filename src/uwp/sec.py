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

    return parse_details(comments, systems)



def get_coords_from_hexnumber(hexnumber: str) -> tuple(int, int):
    x = int(hexnumber[0:2])
    y = int(hexnumber[2:4])
    return (x,y)



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
    system["Hex"] = get_coords_from_hexnumber(cub[1:5])
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



def parse_details(comments: list[str], systems: list[dict]) -> dict:
    """ parse details should provide the 'content' dictionary that
        a space can use to populate itself. """

    space_type = parse_space_type(comments)

    if space_type == "Subsector":
        return parse_subsector(comments, systems)
    elif space_type == "Sector":
        return parse_sector(comments, systems)
    elif space_type == "Domain":
        return parse_domain(comments, systems)
    else:
        raise ValueError(f"(Unknown space type: '{space_type}'")



def parse_name(comments: list[str]) -> str:
    """ Find the first instance of 'Name: ' in the comments.
        This will be the name of the space. """
    name = "Unknown"
    for comment in comments:
        if "Name: " in comment:
            name = comment.replace("Name: ", "").strip()
            break
    return name



def parse_space_type(comments: list[str]) -> str:
    """ Figure out what sort of space this is. Is it:
        A subsector?
        A sector?
        A domain? """
    
    # check for sector
    subsector_count = 0
    for comment in comments:
        if re.match("Subsector [A-P]: ", comment):
            subsector_count += 1

    if subsector_count == 16:
        return "Sector"

    # Check for domain
    subsector_count = 0
    for comment in comments:
        if re.match("Sector [A-D] Subsector [A-P]: ", comment):
            subsector_count += 1

    if subsector_count == 64:
        return "Domain"

    # check for subsector
    subsector_count = 0
    for comment in comments:
        if "Subsector" in comment:
            subsector_count += 1

    if subsector_count == 1:
        return "Subsector"
    else:
        return "Unknown"



def parse_subsector(comments: list[str], systems: list[dict]) -> str:
    """ The simplest type of space to parse: one with no subspaces """
    name = parse_name(comments)

    contents = {
        "Type": "Subsector",
        "Name": name,
        "Systems": systems
    }
    return contents



subsectors_in_a_sector = [
    ['A', 'B', 'C', 'D'],   # coords range from (01,01) to (32,10)
    ['E', 'F', 'G', 'H'],   # coords range from (01,11) to (32,20)
    ['I', 'J', 'K', 'L'],   # coords range from (01,21) to (32,30)
    ['M', 'N', 'O', 'P']    # coords range from (01,31) to (32,40)
    ]

sectors_in_a_domain = [
    ['A', 'B'],             # coords range from (01,01) to (64,40)
    ['C', 'D']              # coords range from (01,41) to (64,80)
    ]

def get_subsector_letter(coords: tuple[int, int]) -> str:
    """ Given the system coordinates, return the subsector letter
        in a sector """
    x = (coords[0] - 1) // 8
    y = (coords[1] - 1) // 10
    return subsectors_in_a_sector[y][x]

def get_sector_and_subsector_letter(coords: tuple[int, int]) -> tuple[str, str]:
    """ Given the system coordinates, return the sector and subsector letters
        in a domain """
    sec_x = (coords[0] - 1) // 32
    sec_y = (coords[1] - 1) // 40
    sub_x = ((coords[0] - 1) % 32) // 8
    sub_y = ((coords[1] - 1) % 40) // 10
    return (sectors_in_a_domain[sec_y][sec_x],
            subsectors_in_a_sector[sub_y][sub_x])

def parse_sector(comments: list[str], systems: list[dict]) -> dict:
    name = parse_name(comments)

    contents = {
        "Type": "Sector",
        "Name": name,
        "Subsectors": []
    }
    """ Use subsector letter as a key """
    subsectors = {}

    for comment in comments:
        if re.match("Subsector [A-P]: ", comment):
            letter = comment[10]
            name = comment[13:].strip()            
            subsector = {
                "Type": "Subsector",
                "Name": name,
                "Systems": []
            }
            subsectors[letter] = subsector

    for system in systems:
        letter = get_subsector_letter(system["Hex"])
        subsectors[letter]["Systems"].append(system)

    for subsector in subsectors.values():
        contents["Subsectors"].append(subsector)
    
    return contents

""" We need sectors denoted like:
    # Sector A: Spinward Marches
    And subsectors denoted like:
    # Sector A Subsector N: District 268
    """
def parse_domain(comments: list[str], systems: list[dict]) -> dict:
    name = parse_name(comments)

    contents = {
        "Type": "Domain",
        "Name": name,
        "Sectors": []
    }

    """ Use sector letter as a key """
    sectors = {}
    """ We can't just use the sector's subsector list yet, as we will
        have to use the subsector letter to index them. """
    subsector_systems = {}


    """ Set up all sectors first, we should not assume they will
        all preceed their subsectors (but in practice this will be true) """
    for comment in comments:
        if re.match("Sector [A-D]: ", comment):
            sector_letter = comment[7]
            name = comment[10:].strip()
            sector = {
                "Type": "Sector",
                "Name": name,
                "Subsectors": []
            }
            sectors[sector_letter] = sector
            """ We'll be putting an entry per subsector in this sector here
                And each will have a list of systems """
            subsector_systems[sector_letter] = {}
    
    for comment in comments:
        if re.match("Sector [A-D] Subsector [A-P]: ", comment):
            sector_letter = comment[7]
            subsector_letter = comment[19]
            name = comment[22:].strip()
            subsector = {
                "Type": "Subsector",
                "Name": name,
                "Systems": []
            }
            """ Set up space for this subsectors systems """
            subsector_systems[sector_letter][subsector_letter] = []

    for system in systems:
        sector_letter, subsector_letter = \
                get_sector_and_subsector_letter(system)
        subsector_systems[sector_letter][subsector_letter].append(system)



    return contents




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


