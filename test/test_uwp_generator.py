""" For testing src/uwp/uwp_generator.py """

import pytest
import src.uwp.uwp_generator as generator
from src.utils.ehex import Ehex
from src.uwp.uwp import check_is_uwp_string_valid as check_uwp_str



@pytest.mark.parametrize("dice_roll, expected",
    [   (2, '0'), (7, '5'), (12, 'A')    ])
def test_generate_size(mocker, dice_roll, expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_size() == expected



@pytest.mark.parametrize("dice_roll, size, space_opera, expected",
    [   
        (2, Ehex('0'), False, '0'),
        (12,Ehex('0'), False, '5'),
        (7, Ehex('7'), False, '7'),
        (12,Ehex('A'), False, 'F'),
        (12,Ehex('0'), True,  '0'),
        (12,Ehex('2'), True,  '0'),
        (5, Ehex('4'), True,  '0'),
        (8, Ehex('4'), True,  '1'),
        (12,Ehex('4'), True,  'A'),
        (7, Ehex('7'), True,  '7')
    ])
def test_generate_atmosphere(mocker, dice_roll, size, space_opera, expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_atmosphere(
            size, space_opera) == expected



@pytest.mark.parametrize("dice_roll, atmosphere, expected",
    [   
        (2, Ehex('0'), "Frozen"),
        (4, Ehex('2'), "Frozen"),
        (3, Ehex('5'), "Frozen"),
        (4, Ehex('0'), "Cold"),
        (6, Ehex('3'), "Cold"),
        (5, Ehex('4'), "Cold"),
        (3, Ehex('8'), "Cold"),
        (2, Ehex('A'), "Cold"),
        (5, Ehex('0'), "Temperate"),
        (7, Ehex('3'), "Temperate"),
        (6, Ehex('E'), "Temperate"),
        (7, Ehex('9'), "Temperate"),
        (6, Ehex('D'), "Temperate"),
        (2, Ehex('B'), "Temperate"),
        (10,Ehex('6'), "Hot"),
        (12,Ehex('2'), "Hot"),
        (11,Ehex('4'), "Hot"),
        (9, Ehex('8'), "Hot"),
        (8, Ehex('F'), "Hot"),
        (4, Ehex('C'), "Hot"),
        (12,Ehex('7'), "Boiling"),
        (12,Ehex('3'), "Hot"),
        (12,Ehex('E'), "Hot"),
        (12,Ehex('8'), "Boiling"),
        (12,Ehex('A'), "Boiling"),
        (12,Ehex('B'), "Boiling")
     ])
def test_generate_temperature(mocker, dice_roll, atmosphere, expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_temperature(atmosphere) == expected
  

@pytest.mark.parametrize(
    "dice_roll, size, atmosphere, temperature, space_opera, expected",
    [   
        (12,Ehex('0'), Ehex('0'), "Frozen",     False, '0'),
        (7, Ehex('7'), Ehex('1'), "Temperate",  False, '3'),
        (7, Ehex('7'), Ehex('6'), "Temperate",  False, '7'),
        (7, Ehex('7'), Ehex('6'), "Hot",        False, '5'),
        (7, Ehex('7'), Ehex('6'), "Boiling",    False, '1'),
        (7, Ehex('7'), Ehex('D'), "Boiling",    False, '7'),
        (12,Ehex('4'), Ehex('A'), "Cold",       False, '5'),
        (12,Ehex('4'), Ehex('A'), "Cold",       True,  '0'),
        (12,Ehex('9'), Ehex('1'), "Cold",       True,  '4'),
        (12,Ehex('9'), Ehex('2'), "Cold",       True,  'A'),
        (3, Ehex('9'), Ehex('A'), "Cold",       True,  '1'),
        (9, Ehex('9'), Ehex('B'), "Cold",       True,  '3')
     ])       
def test_generate_hydrosphere(
        mocker, dice_roll, size, atmosphere, temperature, space_opera,
        expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_hydrosphere(
            size, atmosphere, temperature, space_opera) == expected



@pytest.mark.parametrize(
    "dice_roll, size, atmosphere, hard_science, expected",
    [   
        (2, Ehex('0'), Ehex('0'),   False, '0'),
        (7, Ehex('6'), Ehex('6'),   False, '5'),
        (12,Ehex('8'), Ehex('8'),   False, 'A'),
        (6, Ehex('0'), Ehex('0'),   True,  '2'),
        (7, Ehex('8'), Ehex('6'),   True,  '6'),
        (12,Ehex('8'), Ehex('6'),   True,  'A'),
        (12,Ehex('8'), Ehex('7'),   True,  '9')
     ])
def test_generate_population(
        mocker, dice_roll, size, atmosphere, hard_science, expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_population(
            size, atmosphere, hard_science) == expected



@pytest.mark.parametrize("dice_roll, population, expected",
    [   
        (6, Ehex('7'), '6'),
        (3, Ehex('2'), '0'),
        (12,Ehex('A'), 'F')
     ]) 
def test_generate_government(mocker, dice_roll, population, expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_government(population) == expected



@pytest.mark.parametrize("dice_roll, population, government, expected",
    [   
        (6, Ehex('0'), Ehex('0'), '0'),
        (12,Ehex('0'), Ehex('F'), '0'),
        (2, Ehex('2'), Ehex('0'), '0'),
        (9, Ehex('2'), Ehex('0'), '2'),
        (7, Ehex('7'), Ehex('7'), '7'),
        (9, Ehex('A'), Ehex('A'), 'C'),
        (12,Ehex('A'), Ehex('F'), 'K')
     ]) 
def test_generate_law_level(
        mocker, dice_roll, population, government, expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_law_level(population, government) == expected



""" We ignore the 'hard science' flag as it doesn't combine well with
    mgt2e. Just ignoring it gives perfectly reasonable results. """
@pytest.mark.parametrize(
    "dice_roll, population, hard_science, maturity, expected",
    [
        (6, Ehex('0'), False, "Standard", 'X'),
        (6, Ehex('2'), False, "Standard", 'E'),
        (6, Ehex('2'), False, "Cluster",  'D'),
        (7, Ehex('4'), False, "Standard", 'D'),
        (7, Ehex('4'), False, "Cluster",  'C'),
        (8, Ehex('6'), False, "Standard", 'C'),
        (8, Ehex('8'), False, "Standard", 'B'),
        (10,Ehex('6'), False, "Standard", 'B'),
        (12,Ehex('A'), False, "Cluster",  'A'),
        (11,Ehex('9'), False, "Standard", 'A')
    ])                         
def test_generate_starport(
        mocker, dice_roll, population, hard_science, maturity, expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_starport(
            population, hard_science, maturity) == expected

""" Our lines run a little long here but keeping one line per test makes
    the whole thing much more readable.
    For the last test the mock doesn't quite work, and we have to cheat by
    giving it the correct value (1) to return. The mock doesn't realise that
    generate_tech_level will call dice.roll with an argument of 1 instead of 6
    """
@pytest.mark.parametrize(
    """dice_roll,
    starport, size, atmosphere, hydrosphere, population, government,
    tech_cap, expected""",
    [   #  Starport  Size      Atmo      Hydro     Pop       Gov       Cap  Exp
        (1,Ehex('X'),Ehex('0'),Ehex('0'),Ehex('0'),Ehex('0'),Ehex('0'),None,'0'),
        (6,Ehex('X'),Ehex('8'),Ehex('6'),Ehex('7'),Ehex('0'),Ehex('0'),None,'0'),
        (1,Ehex('E'),Ehex('8'),Ehex('6'),Ehex('7'),Ehex('6'),Ehex('4'),None,'1'),
        (6,Ehex('C'),Ehex('0'),Ehex('0'),Ehex('0'),Ehex('5'),Ehex('5'),None,'E'),
        (6,Ehex('B'),Ehex('8'),Ehex('6'),Ehex('A'),Ehex('A'),Ehex('A'),None,'G'),
        (6,Ehex('A'),Ehex('8'),Ehex('6'),Ehex('A'),Ehex('A'),Ehex('7'),None,'K'),
        (6,Ehex('A'),Ehex('0'),Ehex('0'),Ehex('0'),Ehex('A'),Ehex('7'),None,'M'),
        (6,Ehex('A'),Ehex('0'),Ehex('0'),Ehex('0'),Ehex('A'),Ehex('7'),15,  'H'),
        (1,Ehex('A'),Ehex('8'),Ehex('6'),Ehex('A'),Ehex('A'),Ehex('7'),15,  'F')
    ])
def test_generate_tech_level(
        mocker, dice_roll, 
        starport, size, atmosphere, hydrosphere, population, government,
        tech_cap, expected):
    mock_dice = mocker.patch("src.utils.dice.roll")
    mock_dice.return_value = dice_roll
    assert generator._generate_tech_level(
            starport, size, atmosphere, hydrosphere, population, government,
            tech_cap) == expected


""" We've already tested all the components, we mostly just want to make sure
    we get a valid looking UWP here. So rather than mocking and trying
    to work out what a given set of dice rolls should result in, lets just
    generate a few (hundred) real uwps and use the uwp validator to check 
    them. So no 'expected' here, we'll just run the validator. """
@pytest.mark.parametrize(
    "space_opera, hard_science, maturity, tech_cap",
    [
        (False, False, "Standard", None),
        (True, False, "Mature", None),
        (True, True, "Standard", None),
        (True, True, "Backwater", 12)
    ])
def test_generate_uwp(space_opera, hard_science, maturity, tech_cap):
    for i in range(1, 100):
        uwp = generator.generate_uwp(
                space_opera, hard_science, maturity, tech_cap)
        uwp_str = str(uwp)
        assert check_uwp_str(uwp_str)

