""" Script for describing traveller Spaces.

Spaces include simple spaces such as Subsectors and more complex
spaces such as Sectors and Domains which contain other spaces. """

import json
import sys
from src.utils.dice import roll
from src.uwp.system import System



density_dm = {
            "Rift": -2,     # 6+    16.67%
            "Sparse": -1,   # 5+    33.33%
            "Standard": 0,  # 4+    50%
            "Dense": +1     # 3+    66.67%
        }

def get_system_presence(density: str) -> bool:
    if roll(1, 6) + density_dm[density] >= 4:
        return True
    return False



default_details = {
    "Name": "Space",
    "Density": "Standard",
    "Maturity": "Standard",
    "Space_Opera": False,
    "Hard_Science": False,
    "Tech Cap": None
    }


class Space:
    """ A space is a 2D hexagonal grid that contains systems """

    def __init__(self, 
                 size: tuple(int, int) = (8,10), 
                 origin: tuple(int, int) = (0,0),
                 details: dict = None,
                 contents: dict = None):
        self.size = size
        self.origin = origin
        """ We do have to hang on to details because at a later point we
            may add a new system to generate, and we will need the details
            then. """
        self.details = details
        if details and not contents:
            """ Generate new space contents based on provided details"""
            self.generate()
        elif contents:
            """ Populate the space with the given contents """
            self.populate(contents)
        else:
            raise ValueError("A space must have details or contents")

    def populate(self, contents: dict):
        """ Populates the space with the given contents """
        self.name = contents["Name"]
        self.systems = []
        for system_contents in contents["Systems"]:
            name = system_contents["Name"]
            x,y = system_contents["Hex"]
            system = System(name, (x,y), contents = system_contents)
            self.systems.append(system)

    def generate(self):
        """ Creates new systems with which to populate the space """
        self.name = self.details["Name"]
        self.systems = []
        systems = 0
        for row in range(1, self.size[0]+1):
            for column in range(1, self.size[1]+1):
                if get_system_presence(self.details["Density"]):
                    systems += 1
                    s = System(
                            name = f"{self.details['Name']} {systems}",
                            coordinates = (row + self.origin[0], 
                                           column + self.origin[1]),
                            space_details = self.details)
                    self.systems.append(s)

    def __str__(self):
        """ Prints out for .sec file """
        ret = f"# Name: {self.name}\n"
        for system in self.systems:
            ret += system.__str__() + "\n"
        return ret


class Subsector(Space):
    """ A Subsector is 8x10 hexes """
    size = (8, 10)

    def __init__(self,
                 origin: tuple(int, int) = (0,0),
                 details: dict = default_details,
                 contents: dict = None):
        super().__init__(size = (8, 10), 
                         origin = origin, 
                         details = details, 
                         contents = contents)

    def __str__(self) -> str:
        ret = "# Subsector\n"
        ret += super().__str__()
        return ret


class ContainerOfSpaces(Space):
    """ This is a space that contains other spaces.

    In practice this will be one of two things:
    1) A Sector that contains sixteen Subsectors
    2) A Domain that contains four Sectors

    Yes there is such a thing as a Quadrant of four Subsectors but we
    shall leave that for a future version.

    A ContainerOfSpaces will also be able to contain other
    ContainerOfSpaces e.g. a domain contains sectors contains subsectors.

    Some concepts.
    Base: All ContainerOfSpaces will contain a square number of spaces,
    i.e. 2x2, 4x4. Base is the number to be squared. So a ContainerOfSpaces
    contains base*base subspaces.

    Origin: The coordinate of the space within a larger space. This
    gives context to the coordinates within the space, which can go from
    origin+1 to size

    Subspace Size is the size of the subspaces this space contains.
    The overall size of the this space is:
        (subspace_size[0] * base, subspace_size[1] * base)

    details or contents:
    Details tell us how to create the systems in the space.
    contents tell us about the systems already there.

    details: A ContainerOfSpaces may, or may not, have a "Subspace Details"
    key. If present, it will give a list of the details of its subspaces.
    If not, the subspace details will be derrived from the container space
    details.
    """

    subspace_labels = [
        'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P'
        ]
    
    def __init__(self,
                 base: int,
                 origin: tuple[int, int] = (0,0),
                 subspace_size: tuple[int, int] = (8, 10),
                 subspace_descriptor:str = "Subspace",
                 details: dict = None,
                 contents: dict = None):

        self.base = base
        self.num_subspaces = base ** 2
        self.subspace_size = subspace_size
        self.subspace_descriptor = subspace_descriptor

        super().__init__(
            size = (subspace_size[0] * base, subspace_size[1] * base), # Size
            origin = origin,
            details = details,
            contents = contents
            )

    def get_subspace_descriptor(self) -> str:
        return self.subspace_descriptor

    def get_subspace_list(self) -> str:
        return self.get_subspace_descriptor() + "s"

    def get_subspace_index(self, row: int, column: int) -> int:
        return (row * self.base) + column
    
    def get_subspace_origin(self, row: int, column: int) -> tuple[int, int]:
        """ Rememer that hex coordinates are column,row """
        return (self.origin[0] + (column * self.subspace_size[0]),
                self.origin[1] + (row * self.subspace_size[1]))

    def populate(self, contents: dict):
        self.name = contents["Name"]
        self.subspaces = []
        for row in range(self.base):
            for column in range(self.base):
                i = self.get_subspace_index(row, column)
                origin = self.get_subspace_origin(row, column)
                subspace = self.populate_subspace(
                        origin,
                        contents[self.get_subspace_list()][i])
                self.subspaces.append(subspace)

    def populate_subspace(self, origin: tuple[int, int], contents: dict):
        return Space(self.subspace_size, origin, contents = contents)

    def generate(self):
        self.name = self.details["Name"]
        self.subspaces = []
        for row in range(self.base):
            for column in range(self.base):
                index = self.get_subspace_index(row, column)
                origin = self.get_subspace_origin(row, column)

                if self.get_subspace_list() in self.details:
                    details = self.details[self.get_subspace_list()][index]
                else:
                    details = {}
                """ We allow the user to omit fields so they need only
                    fill those that are important """
                self.autofill_subspace_details(details, index)

                subspace = self.generate_subspace(origin, details)
                self.subspaces.append(subspace)

    def autofill_subspace_details(self, details: dict, index: int):
        """ Automatically fills any omitted subspace details with details
            from the parent space """
        fields_to_copy = [
            "Density",
            "Maturity",
            "Space Opera",
            "Hard Science",
            "Tech Cap"
        ]

        if not "Name" in details:
            details["Name"] = \
               f"{self.name} {self.get_subspace_descriptor()} " \
               f"{self.subspace_labels[index]}"
        if not "Type" in details:
            details["Type"] = self.get_subspace_descriptor()

        for field in fields_to_copy:
            if field not in details:
                details[field] = self.details[field]


    def generate_subspace(self, origin: tuple[int, int], details: dict):
        return Space(self.subspace_size, origin, details = details)

    def __str__(self):
        ret = f"# Space: {self.name}\n"
        for subspace in self.subspaces:
            ret += subspace.__str__()
        return ret


    def __str__(self):
        ret = f"# {self.__class__.__name__}\n# Name: {self.name}\n"
        for i, subspace in enumerate(self.subspaces):
            ret += f"# {self.subspace_descriptor} "
            ret += f"{self.subspace_labels[i]}: "
            ret += f"{subspace.name}\n"
            ret += subspace.__str__()
        return ret



class Sector(ContainerOfSpaces):
    """ A sector contains 16 subsectors """

    """ A Sector is 32x40 hexes """
    size = (32, 40)

    def __init__(self, 
                 origin: tuple[int, int] = (0,0),
                 details: dict = None,
                 contents: dict = None):
        super().__init__(
            base = 4,              # 4x4 subsectors
            origin = origin,
            subspace_size = Subsector.size, # Subsector Size
            subspace_descriptor = "Subsector",
            details = details,
            contents = contents
            )

    def populate_subspace(self, origin: tuple[int, int], contents: dict):
        return Subsector(origin, contents = contents)

    def generate_subspace(self, origin: tuple[int, int], details: dict):
        return Subsector(origin, details = details)


    
class Domain(ContainerOfSpaces):
    """ A Domain contains 4 sectors """

    def __init__(Self,
                 details: dict = None,
                 contents: dict = None):
        super().__init__(
            base = 2,           # 2x2 sectors
            origin = (0,0),     # Domains is the top level of space
            subspace_size = Sector.size,
            subspace_descriptor = "Sector",
            details = details,
            contents = contents
            )

    def populate_subspace(self, origin: tuple[int, int], contents: dict):
        return Sector(origin, contents = contents)

    def generate_subspace(self, origin: tuple[int, int], details: dict):
        return Sector(origin, details = details)



def create_space_from_contents(contents: dict) -> Space:
    """ Create a new space object given the space contents i.e.
        already generated systems """
    space_type = contents["Type"]
    if space_type == "Subsector":
        return Subsector(origin = (0, 0), contents = contents)
    elif space_type == "Sector":
        return Sector(origin = (0, 0), contents = contents)
    elif space_type == "Domain":
        return Domain(contents = contents)
    else:
        raise ValueError(f"Got space type: '{space_type}'."\
                "I expect a Subsector, Sector, or Domain.")



def create_space_from_details(details: dict) -> Space:
    """ Create a new space object given the space details i.e.
        instructions on how to generate systems """
    space_type = details["Type"]
    if space_type == "Subsector":
        return Subsector(origin = (0, 0), details = details)
    elif space_type == "Sector":
        return Sector(origin = (0, 0), details = details)
    elif space_type == "Domain":
        return Domain(details = details)
    else:
        raise ValueError(f"Got space type: '{space_type}'."\
                "I expect a Subsector, Sector, or Domain.")


def create_space_from_json(buffer: str) -> Space:
    details = json_to_details(buffer)
    if details:
        return create_space_from_details(details)
    else:
        raise ValueError("Got bad details from json")
    


def json_to_details(buffer: str) -> dict:
    details = json.loads(buffer)
    if check_details(details):
        return details
    else:
        return None


default_details = {
    "Density": "Standard",
    "Maturity": "Standard",
    "Space Opera": False,
    "Hard Science": False,
    "Tech Cap": None
}

def check_details(details: dict) -> bool:
    """ The only fields we absolutely need are name and type. """
    if not "Name" in details:
        return False
    if not "Type" in details:
        return False

    """ We can leave fields blank if they are just the default """
    for detail in default_details:
        if not detail in details:
            details[detail] = default_details[detail]

    return True
