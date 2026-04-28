""" For testing src/uwp/uwp.py """

from contextlib import nullcontext
import pytest
import src.uwp.uwp as uwp
from src.uwp.uwp import Uwp
from src.utils.ehex import Ehex



@pytest.mark.parametrize("test_value, expected",
    [   ("A867A77-8", True),
        ("F867A77-8", False),
        ("Clearly not a UWP", False),
        (12, False),
        ((Ehex('B'), Ehex('A'), Ehex('A'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9'), Ehex('F')),
         False),
        ({"Starport": Ehex('C'),
          "Size": Ehex('7'),
          "Atmosphere": Ehex('5'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('6'),
          "Law Level": Ehex('4'),
          "Tech Level": Ehex('8')},
         False)
    ])
def test_check_is_uwp_string_valid(test_value, expected):
    assert uwp.check_is_uwp_string_valid(test_value) == expected



@pytest.mark.parametrize("test_value, expected",
    [   ("A867A77-8", False),
        (12, False),
        ((Ehex('B'), Ehex('A'), Ehex('A'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9'), Ehex('F')),
         True),
        ((Ehex('H'), Ehex('A'), Ehex('A'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9'), Ehex('F')),
         False),
        (('A', '8', '6', '7', 'A', '7', '7', '8'),
         False),
        ((Ehex('B'), Ehex('A'), Ehex('A'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9')),
         False),
        ((Ehex('B'), Ehex('A'), Ehex('A'), Ehex('0'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9'), Ehex('F')),
         False),
        ({"Starport": Ehex('C'),
          "Size": Ehex('7'),
          "Atmosphere": Ehex('5'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('6'),
          "Law Level": Ehex('4'),
          "Tech Level": Ehex('8')},
         False)
    ])
def test_check_is_uwp_tuple_valid(test_value, expected):
    assert uwp.check_is_uwp_tuple_valid(test_value) == expected



@pytest.mark.parametrize("test_value, expected",
    [   ("A867A77-8", False),
        (12, False),
        ((Ehex('B'), Ehex('A'), Ehex('A'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9'), Ehex('F')),
         False),
        ({"Starport": Ehex('C'),
          "Size": Ehex('7'),
          "Atmosphere": Ehex('5'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('6'),
          "Law Level": Ehex('4'),
          "Tech Level": Ehex('8')},
         True),
        ({"Starport": Ehex('M'),    """ Starport out of bounds """
          "Size": Ehex('7'),
          "Atmosphere": Ehex('5'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('6'),
          "Law Level": Ehex('4'),
          "Tech Level": Ehex('8')},
         False),
        ({"Starport": Ehex('C'),
          "Size": Ehex('7'),
          """ Missing Atmosphere """
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('6'),
          "Law Level": Ehex('4'),
          "Tech Level": Ehex('8')},
         False),
        ({"Startport": Ehex('C'),   """ Typo """
          "Size": Ehex('7'),
          "Atmosphere": Ehex('5'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('6'),
          "Law Level": Ehex('4'),
          "Tech Level": Ehex('8')},
         False),
        ({"Starport": Ehex('C'),
          "Size": Ehex('7'),
          "Atmosphere": Ehex('5'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('6'),
          "Law Level": Ehex('4'),
          "Tech Level": Ehex('8'),
          """ We don't care about extra fields """
          "Not a UWP": Ehex('0')},
         True)
    ])
def test_check_is_uwp_dict_valid(test_value, expected):
    assert uwp.check_is_uwp_dict_valid(test_value) == expected
    


@pytest.mark.parametrize("test_value, expected",
    [   ("A867A77-8", nullcontext()),
        ("F867A77-8", pytest.raises(ValueError)),
        ("Clearly not a UWP", pytest.raises(ValueError)),
        ((Ehex('B'), Ehex('A'), Ehex('A'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9'), Ehex('F')),
         nullcontext()),
        ((Ehex('H'), Ehex('A'), Ehex('A'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9'), Ehex('F')),
         pytest.raises(ValueError)),
        ({"Starport": Ehex('B'),
          "Size": Ehex('0'),
          "Atmosphere": Ehex('0'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('5'),
          "Law Level": Ehex('3'),
          "Tech Level": Ehex('A')},
         nullcontext()),
        ({"Starport": Ehex('Z'),
          "Size": Ehex('0'),
          "Atmosphere": Ehex('0'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('5'),
          "Law Level": Ehex('3'),
          "Tech Level": Ehex('A')},
         pytest.raises(ValueError)),
        (12, pytest.raises(TypeError))
    ])
def test_uwp_creation(test_value, expected):
    with expected as e:
        my_uwp = Uwp(test_value)


@pytest.mark.parametrize("test_value, expected",
    [   (Uwp("A867A77-8"), "A867A77-8"),
        (Uwp((Ehex('B'), Ehex('A'), Ehex('A'), Ehex('0'),
          Ehex('8'), Ehex('8'), Ehex('9'), Ehex('F'))),
         "BAA0889-F"),
        (Uwp({"Starport": Ehex('B'),
          "Size": Ehex('0'),
          "Atmosphere": Ehex('0'),
          "Hydrosphere": Ehex('0'),
          "Population": Ehex('6'),
          "Government": Ehex('5'),
          "Law Level": Ehex('3'),
          "Tech Level": Ehex('A')}),
         "B000653-A")        
    ])
def test_uwp_str(test_value, expected):
    assert str(test_value) == expected
