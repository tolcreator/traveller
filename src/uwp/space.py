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



default_space_details = {
        "Density": "Standard",
        "Maturity": "Standard",
        "Space_Opera": False,
        "Hard_Science": False,
        "Tech Cap": None
        }

class Space:
    """ A space is a 2D hexagonal grid that contains systems """

    def __init__(self, 
                 name: str, 
                 size: tuple(int, int) = (8,10), 
                 origin: tuple(int, int) = (0,0),
                 details: dict = default_space_details,
                 contents: dict = None):
        self.name = name
        self.size = size
        self.origin = origin
        self.details = details
        if contents:
            """ Populate the space with the given contents """
            self.populate(contents)
        else:
            """ Generate new space contents """
            self.generate()

    def populate(self, contents: dict):
        """ Populates the space with the given contents """
        self.systems = []
        for system_contents in contents["Systems"]:
            name = system_contents["Name"]
            hex_number = system_contents["Hex"]
            x = int(hex_number[0:2])
            y = int(hex_number[2:4])
            system = System(name, (x,y), contents = system_contents)
            self.systems.append(system)

    def generate(self):
        """ Creates new systems with which to populate the space """
        self.systems = []
        systems = 0
        for row in range(1, self.size[0]+1):
            for column in range(1, self.size[1]+1):
                if get_system_presence(self.details["Density"]):
                    systems += 1
                    s = System(
                            name = f"{self.name} {systems}",
                            coordinates = (row + self.origin[0], 
                                           column + self.origin[1]),
                            space_details = self.details)
                    self.systems.append(s)

    def __str__(self):
        """ Prints out for .sec file """
        ret = ""
        for system in self.systems:
            ret += system.__str__() + "\n"
        return ret

