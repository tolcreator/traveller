""" Script for handling traveller Systems. 

This should:
    1)  Generate system data
    2)  Convert that data into a line of a .sec file
    3)  Be a handy container of system data for use elsewhere

We want to either provide the system object with some formatted data - which
we may have read from a file for example, and have it use that to create the
system object, or generate the system.

"""

from src.utils.dice import roll
from src.utils.ehex import Ehex
from src.uwp.uwp import Uwp
from src.uwp.uwp_generator import generate_uwp
from src.uwp.ct_book_six import (
        generate_stellar_data,
        generate_planetoid_belts,
        generate_gas_giants)


class System:
    def __init__(self, 
                 name: str, 
                 coordinates: tuple[int, int], 
                 system_details: dict = None,
                 space_details: dict = None):

        """ We cannot generate a name, this MUST be provided """
        self.name = name
        """ We cannot generate coordinates, these MUST be provided """
        self.coordinates = coordinates

        if system_details:
            """ Fill out the system object with the details given """
            self.uwp = Uwp(system_details["uwp"])
            self.parse_bases(system_details["bases"])
            self.parse_zone(system_details["zone"])
            self.parse_pbg(system_details["pbg"])
            self.parse_allegiance(system_details["allegiance"])
            self.parse_stellar(system_details["stellar"])
        else:
            """ Generate the system given the space details """
            if not space_details:
                self.uwp = generate_uwp()
            else:
                self.uwp = generate_uwp(
                        space_opera = space_details["Space Opera"],
                        hard_science = space_details["Hard Science"],
                        maturity = space_details["Maturity"],
                        tech_cap = space_details["Tech Cap"])
            self.generate_bases()
            self.generate_pbg()
            self.generate_stellar()
            """ Note that we cannot generate zone or allegiance either """
            """ TODO work out how to set these """
            self.zone = None
            self.allegiance = None

        """ Trade codes are expensive to calculate so we need to have them
            on hand rather than calculating them every time we are asked. """
        self.update_trade_codes()

    def generate_bases(self):
        """ Using Classic Traveller rules """
        # First discover if we have a naval base
        if self.uwp.starport in ['A', 'B'] and roll(2, 6) >= 8:
            self.naval_base = True
        else:
            self.naval_base = False

        # Then figure out if we have a scout base
        scout_dm = 0
        if self.uwp.starport == 'C':
            scout_dm = -1
        elif self.uwp.starport == 'B':
            scout_dm = -2
        elif self.uwp.starport == 'A':
            scout_dm = -3

        if self.uwp.starport in ['A', 'B', 'C', 'D'] and \
            (roll(2, 6) + scout_dm) >= 7:
            self.scout_base = True
        else:
            self.scout_base = False

    def generate_pbg(self):
        """ P = Population Multiplier
            B = Belts (i.e. Planetoid Belts)
            G = Gas Giants """

        # Population multiplier
        # We don't have to torture ourselves by trying to get d6s to emulate
        # other dice types
        if self.uwp.population > 0:
            self.population_multiplier = roll(1, 9)
        else:
            self.population_multiplier = 0

        self.belts = generate_planetoid_belts()
        if self.uwp.size == "0" and self.belts == 0:
            self.belts = 1

        self.gas_giants = generate_gas_giants()

    def generate_stellar(self):
        self.stars = generate_stellar_data(self.uwp)

    def parse_bases(self, base_code: str):
        """ For now we only accept the following base codes:
            N: Naval Base
            S: Scout Base
            B: Both """

        if base_code in ["N", "B"]:
            self.naval_base = True
        else:
            self.naval_base = False
        if base_code in ["S", "B"]:
            self.scout_base = True
        else:
            self.scout_base = False

    def parse_zone(self, zone: str):
        self.zone = zone

    def parse_pbg(self, pbg: str):
        p = pbg[0]
        b = pbg[1]
        g = pbg[2]
        self.population_multiplier = int(p)
        self.belts = int(b)
        self.gas_giants = int(g)

    def parse_allegiance(self, allegiance: str):
        self.allegiance = allegiance

    def parse_stellar(self, stellar: str):
        """ TODO parse stellar data """
        self.stars = []
        chunks = stellar.split()
        while(chunks):
            chunk = chunks.pop(0)
            if chunk[0] in "OBAFGKM":
                """ This chunk is a stellar type/class pair """
                star = chunk
                if star[1] == "D":
                    "We ignore White Dwarf stellar type"
                    star = "D"
                else:
                    """ Pick up stellar size """
                    chunk = chunks.pop(0)
                    star += " " + chunk
            elif chunk == "D":
                star = chunk
            else:
                raise ValueError(
                    f"Don't know how to deal with star chunk '{chunk}' " \
                    f"in stellar data '{stellar}'")
            self.stars.append(star)
        

    def update_trade_codes(self):
        """ TODO update trade codes """
        """ This should be called whenever uwp is set """
        pass

    def get_base_code(self) -> str:
        if self.naval_base and self.scout_base:
            return 'B'
        if self.naval_base:
            return 'N'
        if self.scout_base:
            return 'S'
        return ' '

    def get_trade_codes_str(self) -> str:
        """ TODO get trade codes str """
        return ""

    def get_zone_str(self) -> str:
        if self.zone:
            return self.zone
        else:
            return " "            

    def get_pbg_str(self) -> str:
        return "{}{}{}".format(
                self.population_multiplier,
                self.belts,
                self.gas_giants)

    def get_allegiance_str(self) -> str:
        if self.allegiance:
            return self.allegiance
        else:
            return "Na"

    def get_stellar_str(self) -> str:
        ret = ""
        for star in self.stars:
            ret += f"{star} "
        return ret

    def __str__(self) -> str:
        """ Should return a valid line for a .sec file """
        return  f"{self.name:<14}" \
                f"{self.coordinates[0]:02d}{self.coordinates[1]:02d} " \
                f"{self.uwp}  " \
                f"{self.get_base_code()} " \
                f"{self.get_trade_codes_str():<15} " \
                f"{self.get_zone_str():<2} " \
                f"{self.get_pbg_str()} " \
                f"{self.get_allegiance_str():<2} " \
                f"{self.get_stellar_str()}"
