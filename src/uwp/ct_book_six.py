from src.utils.dice import roll
from src.utils.ehex import Ehex
from src.uwp.uwp import Uwp

""" Stellar Data from Book 6: Scouts """

sft = {
    "Basic Nature": [
    #    0       1       2       3       4       5       6       
        "Solo", "Solo", "Solo", "Solo", "Solo", "Solo", "Solo",
    #    7       8         9         10        11        12
        "Solo", "Binary", "Binary", "Binary", "Binary", "Trinary"],
    "Primary Type": [
    #    0    1    2    3    4    5    6    7    8    9    10   11   12
        "B", "B", "A", "M", "M", "M", "M", "M", "K", "G", "G", "F", "F"],
    "Primary Size": [
    #    0     1     2     3      4     5    6    7    8    9    10   11   12
        "Ia", "Ib", "II", "III", "IV", "V", "V", "V", "V", "V", "V", "V", "V"],
    "Companion Type": [
    #    0    1    2    3    4    5    6    7    8    9    10   11   12
        "-", "B", "A", "F", "F", "G", "G", "K", "K", "M", "M", "M", "M"],
    "Companion Size": [
    #    0     1     2     3      4     5    6    7    8    9    10   11   12
        "Ia", "Ib", "II", "III", "IV", "V", "V", "V", "V", "V", "V", "V", "D"],
    "Companion Orbit": [
    #    0        1        2        3        4    5    6    7     8     9
        "Close", "Close", "Close", "Close", "1", "2", "3", "4+", "5+", "6+",
    #    10    11    12
        "7+", "8+", "Far"],
    "Gas Giant Presence": [
    #   0     1     2     3     4     5     6     7     8     9
        True, True, True, True, True, True, True, True, True, True,
    #   10     11     12
        False, False, False],
    "Gas Giant Quantity": [
    #    0    1    2    3    4    5    6    7    8    9    10   11   12
         1,   1,   1,   1,   2,   2,   3,   3,   4,   4,   4,   5,   5],
    "Planetoid Belt Presence": [
    #   0     1     2     3     4     5     6
        True, True, True, True, True, True, True,
    #   7      8      9      10     11     12
        False, False, False, False, False, False],
    "Planetoid Belt Quantity": [
    #    0  1  2  3  4  5  6  7  8  9  10 11 12
         3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1]
    }

def sft_lookup(field: str, result: int):
    """ A sanitised 'in' to the system feature table """
    table = sft[field]
    if result >= len(table):
        return table[-1]
    else:
        return table[result]


def generate_planetoid_belts():
    if sft_lookup("Planetoid Belt Presence", roll(2, 6)):
        return sft_lookup("Planetoid Belt Quantity", roll(2, 6))
    return 0

def generate_gas_giants():
    if sft_lookup("Gas Giant Presence", roll(2, 6)):
        return sft_lookup("Gas Giant Quantity", roll(2, 6))
    return 0

def generate_stellar_data(uwp: Uwp) -> list[str]:
    """ Using Classic Traveller, and the Errata """
    
    basic_nature = sft_lookup("Basic Nature", roll(2, 6))
    dm = 0
    if uwp.atmosphere in ["4", "5", "6", "7", "8", "9"] or \
        uwp.population >= 8:
            dm = 5
    return generate_stars(basic_nature, dm, dm, True, 0)

def generate_stars(basic_nature: str,
                   type_dm: int = 0,
                   size_dm: int = 0,
                   primary: bool = False,
                   orbit_dm: int = 0) -> list[str]:
    type_roll = roll(2, 6) + type_dm
    size_roll = roll(2, 6) + size_dm

    if primary:
        star_type = sft_lookup("Primary Type", type_roll)
        size = sft_lookup("Primary Size", size_roll)
    else:
        star_type = sft_lookup("Companion Type", type_roll)
        size = sft_lookup("Companion Size", size_roll)
        orbit = sft_lookup("Companion Orbit", roll(2, 6) + orbit_dm)
        if orbit == "Far":
            basic_nature = sft_lookup("Basic Nature", roll(2, 6))
            orbit_dm -= 4

    # We have d10s, we don't need to try to emulate them with d6s
    classification = roll(1, 10) - 1
    if size == "IV":
        if star_type == "K" and classification >= 5:
            size = "V"
        if star_type == "M":
            size = "V"

    if size != "D":
        star = f"{star_type}{classification} {size}"
    else:
        star = "D"
    stars = [star]

    """ By RAW these are not divided by 2. But this gives almost
        all companions as White Dwarfs, which does not match with
        canonical data e.g. spinward marches. Even this gives a lot
        more WDs than are in the Spinward Marches """
    type_dm = type_roll // 2
    size_dm = size_roll // 2

    if basic_nature == "Binary":
        stars += generate_stars(
                "Solo", type_dm, size_dm, False, orbit_dm)

    if basic_nature == "Trinary":
        stars += generate_stars(
                "Solo", type_dm, size_dm, False, orbit_dm + 4)

    return stars                    


