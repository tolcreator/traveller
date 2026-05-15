""" Given a UWP returns the trade codes
    Note that this should be done once after a UWP is set up,
    and not called every time the trade codes are needed. They should be
    stored in the system object. This is because working out the trade
    codes is an expensive process that will cripple performence when we do
    intersystem economics later on """

from src.utils.ehex import Ehex
from src.uwp.uwp import Uwp

def get_is_agricultural(uwp: Uwp) -> bool:
    if uwp.atmosphere in ['4', '5', '6', '7', '8', '9'] and \
        uwp.hydrosphere in ['4', '5', '6', '7', '8'] and \
        uwp.population in ['5', '6', '7']:
            return True
    return False

def get_is_asteroid(uwp: Uwp) -> bool:
    if uwp.size == '0' and \
        uwp.atmosphere == '0' and \
        uwp.hydrosphere == '0':
            return True
    return False

def get_is_barren(uwp: Uwp) -> bool:
    if uwp.population == '0' and \
        uwp.government == '0' and \
        uwp.law_level == '0':
            return True
    return False

def get_is_desert(uwp: Uwp) -> bool:
    if uwp.atmosphere >= '2' and \
        uwp.hydrosphere == '0':
            return True
    return False

def get_is_fluid_oceans(uwp: Uwp) -> bool:
    if uwp.atmosphere >= 'A' and \
        uwp.hydrosphere >= '1':
            return True
    return False

def get_is_garden(uwp: Uwp) -> bool:
    if uwp.size in ['6', '7', '8'] and \
        uwp.atmosphere in ['5', '6', '8'] and \
        uwp.hydrosphere in ['5', '6', '7']:
            return True
    return False

def get_is_high_population(uwp: Uwp) -> bool:
    if uwp.population >= '9':
        return True
    return False

def get_is_high_technology(uwp: Uwp) -> bool:
    if uwp.tech_level >= 'C':
        return True
    return False

def get_is_ice_capped(uwp: Uwp) -> bool:
    if uwp.atmosphere in ['0', '1'] and \
        uwp.hydrosphere >= '1':
            return True
    return False

def get_is_industrial(uwp: Uwp) -> bool:
    if uwp.atmosphere in ['0', '1', '2', '4', '7', '9'] and \
        uwp.population >= '9':
            return True
    return False

def get_is_low_population(uwp: Uwp) -> bool:
    if uwp.population <= '3':
        return True
    return False

def get_is_low_technology(uwp: Uwp) -> bool:
    if uwp.tech_level <= '5':
        return True
    return False

def get_is_non_agricultural(uwp: Uwp) -> bool:
    if uwp.atmosphere in ['0', '1', '2', '3'] and \
        uwp.hydrosphere in ['0', '1', '2', '3'] and \
        uwp.population >= '6':
            return True
    return False

def get_is_non_industrial(uwp: Uwp) -> bool:
    if uwp.population <= '6':
        return True
    return False

def get_is_poor(uwp: Uwp) -> bool:
    if uwp.atmosphere in ['2', '3', '4', '5'] and \
        uwp.hydrosphere in ['0', '1', '2', '3']:
            return True
    return False

def get_is_rich(uwp: Uwp) -> bool:
    if uwp.atmosphere in ['6', '8'] and \
        uwp.population in ['6', '7', '8'] and \
        uwp.government in ['4', '5', '6', '7', '8', '9']:
            return True
    return False

def get_is_vacuum(uwp: Uwp) -> bool:
    if uwp.atmosphere == '0':
        return True
    return False

def get_is_water_world(uwp: Uwp) -> bool:
    if uwp.hydrosphere >= 'A':
        return True
    return False

criteria = {
    "Ag": get_is_agricultural,
    "As": get_is_asteroid,
    "Ba": get_is_barren,
    "De": get_is_desert,
    "Fl": get_is_fluid_oceans,
    "Ga": get_is_garden,
    "Hi": get_is_high_population,
    "Ht": get_is_high_technology,
    "Ic": get_is_ice_capped,
    "In": get_is_industrial,
    "Lo": get_is_low_population,
    "Lt": get_is_low_technology,
    "Na": get_is_non_agricultural,
    "Ni": get_is_non_industrial,
    "Po": get_is_poor,
    "Ri": get_is_rich,
    "Va": get_is_vacuum,
    "Wa": get_is_water_world
}

def get_trade_codes(uwp: Uwp) -> list[str]:
    codes = []
    for criterion, evaluator in criteria.items():
        if evaluator(uwp):
            codes.append(criterion)
    return codes














