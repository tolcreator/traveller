""" Group functions for generating UWPs """

""" We are using Mongoose Traveller 2e rules with a few additions
1) We are using 'space opera' and 'hard science' flags from 1e
2) We are using different columns for starport, inspired by those in
Megatraveller """

import src.utils.dice as dice
from src.utils.ehex import Ehex
from src.uwp.uwp import Uwp

""" Note in MT this table runs 2 = 'A' to 12 = 'X', I have reversed it here """
starport_tables = {     # 0   1   2   3   4   5   6   7   8   9   10  11  12
        "Backwater":    ['X','X','X','E','E','D','D','C','C','C','B','B','A'],
        "Standard":     ['X','X','X','E','E','D','D','C','C','B','B','A','A'],
        "Mature":       ['X','X','E','E','E','D','D','C','C','B','B','A','A'],
        "Cluster":      ['X','X','X','E','D','D','C','C','B','B','A','A','A']
        }


def _generate_size() -> Ehex:
    return Ehex(dice.roll(2, 6) - 2)


def _generate_atmosphere(size: Ehex, space_opera: bool) -> Ehex:
    atmo = dice.roll(2, 6) + size - 7
    if atmo < 0:
        return Ehex(0)

    if space_opera:
        if size <= 2:
            return Ehex(0)
        if size in [3, 4]:
            if atmo <= 2:
                return Ehex(0)
            elif atmo <= 5:
                return Ehex(1)
            else:
                return Ehex('A')
    return Ehex(atmo)


def _generate_temperature(atmosphere: Ehex) -> str:
    """ temperature is not part of the UWP but used as a modifier """
    if atmosphere in [2, 3]:
        dm = -2
    elif atmosphere in [4, 5, 'E']:
        dm = -1
    elif atmosphere in [8, 9]:
        dm = 1
    elif atmosphere in ['A', 'D', 'F']:
        dm = 2
    elif atmosphere in ['B', 'C']:
        dm = 6
    else:
        dm = 0

    temp_roll = dice.roll(2, 6) + dm
    if temp_roll <= 2:
        return "Frozen"
    if temp_roll <= 4:
        return "Cold"
    if temp_roll <= 9:
        return "Temperate"
    if temp_roll <= 11:
        return "Hot"
    return "Boiling"


def _generate_hydrosphere(
        size: Ehex, atmosphere: Ehex, 
        temperature: str, space_opera: bool) -> Ehex:
    dm = 0

    if size == 0 or size == 1:
        return Ehex(0)

    if atmosphere in [0, 1, 'A', 'B', 'C']:
        dm += -4

    if atmosphere not in ['D', 'F']:
        if temperature == "Hot":
            dm += -2
        if temperature == "Boiling":
            dm += -6

    if space_opera:
        if size in [3,4] and atmosphere == 'A':
            dm += -6
        if atmosphere in [0, 1]:
            dm += -6
        if atmosphere in [2, 3, 'B', 'C']:
            dm += -4

    hydro = dice.roll(2, 6) - 7 + size + dm

    if hydro < 0:
        return Ehex(0)
    if hydro > 0xA:
        return Ehex('A')
    return Ehex(hydro)


def _generate_population(size: Ehex, atmosphere: Ehex,
                         hard_science: bool) -> Ehex:
    dm = 0
    if hard_science:
        if size <= 2 or size >= 'A':
            dm -= 1
        if atmosphere in [5, 6, 8]:
            dm += 1
        else:
            dm -= 1
    pop = dice.roll(2, 6) - 2 + dm
    if pop < 0:
        return Ehex(0)
    if pop > 0xA:
        return Ehex('A')
    return Ehex(pop)


def _generate_government(population: Ehex) -> Ehex:
    if population == 0:
        return Ehex(0)

    gov = dice.roll(2, 6) - 7 + population
    if gov < 0:
        return Ehex(0)
    return Ehex(gov)


def _generate_law_level(population: Ehex, government: Ehex) -> Ehex:
    if population == 0:
        return Ehex(0)

    law = dice.roll(2, 6) - 7 + government
    if law < 0:
        return Ehex(0)
    return Ehex(law)


def _generate_starport(population: Ehex, hard_science: bool, 
                       maturity: str) -> Ehex:

    """ MGT2e already has modifiers for starport based on population,
    if much more subtle than pop-7. The "Hard Science" result ends 
    up in huge tech levels, as high pop and starport both contribute
    hugely to tech. Just leaving it to MGT2e sans "hard science" gives 
    more regular results. """

    hard_science = False

    if population == 0:
        return Ehex('X')

    starport_table = starport_tables[maturity]

    dm = 0
    if hard_science:
        dm = population - 7
    else:
        if population <= 2:
            dm = -2
        elif population <= 4:
            dm = -1
        elif population >= 'A':
            dm = 2
        elif population >= 8:
            dm = 1

    port_lookup = dice.roll(2, 6) + dm
    if port_lookup >= len(starport_table):
        return Ehex('A')
    if port_lookup < 0:
        port_lookup = 0
    return Ehex(starport_table[port_lookup])


def _get_starport_tech_dm(starport: Ehex) -> int:
    if starport == 'X':
        return -4
    if starport == 'C':
        return 2
    if starport == 'B':
        return 4
    if starport == 'A':
        return 6
    return 0


def _get_size_tech_dm(size: Ehex) -> int:
    if size <= 1:
        return 2
    if size <= 4:
        return 1
    return 0


def _get_atmosphere_tech_dm(atmosphere: Ehex) -> int:
    if atmosphere <= 3 or atmosphere >= 'A':
        return 1
    return 0


def _get_hydrosphere_tech_dm(hydrosphere: Ehex) -> int:
    if hydrosphere in [0, 9]:
        return 1
    if hydrosphere == 'A':
        return 2
    return 0


def _get_population_tech_dm(population: Ehex) -> int:
    if population in [1, 2, 3, 4, 5, 8]:
        return 1
    if population == 9:
        return 2
    if population == 'A':
        return 4
    return 0


def _get_government_tech_dm(government: Ehex) -> int:
    if government in [0, 5]:
        return 1
    if government == 7:
        return 2
    if government in ['D', 'E']:
        return -2
    return 0


def _generate_tech_level(starport: Ehex, size: Ehex, atmosphere: Ehex,
                         hydrosphere: Ehex, population: Ehex, government: Ehex,
                         tech_cap: int) -> Ehex:
    if population == 0:
        return Ehex(0)

    dm = 0
    dm += _get_starport_tech_dm(starport)
    dm += _get_size_tech_dm(size)
    dm += _get_atmosphere_tech_dm(atmosphere)
    dm += _get_hydrosphere_tech_dm(hydrosphere)
    dm += _get_population_tech_dm(population)
    dm += _get_government_tech_dm(government)

    if tech_cap and dm+1 > tech_cap:
        return Ehex(dm + 1)
    elif tech_cap and dm+6 > tech_cap:
        diff = tech_cap - dm
        tech = dice.roll(1, diff) + dm
    else:
        tech = dice.roll(1, 6) + dm
    if tech < 0:
        return Ehex(0)
    return Ehex(tech)


def generate_uwp(space_opera = False, 
                 hard_science = False, 
                 maturity = "Standard",
                 tech_cap = None):
    """ Hard science uses all of the 'space opera' modifiers too """
    if hard_science:
        space_opera = True
    size = _generate_size()
    atmosphere = _generate_atmosphere(size, space_opera)
    temperature = _generate_temperature(atmosphere)
    hydrosphere = _generate_hydrosphere(size, atmosphere,
                                        temperature, space_opera)
    population = _generate_population(size, atmosphere, hard_science)
    government = _generate_government(population)
    law_level = _generate_law_level(population, government)
    starport = _generate_starport(population, hard_science, maturity)
    tech_level = _generate_tech_level(
            starport, size, atmosphere, hydrosphere, 
            population, government, tech_cap)

    return Uwp({
        "Starport": starport,
        "Size": size,
        "Atmosphere": atmosphere,
        "Hydrosphere": hydrosphere,
        "Population": population,
        "Government": government,
        "Law Level": law_level,
        "Tech Level": tech_level
        })
