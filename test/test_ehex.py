""" For testing src/utils/ehex.py """

from contextlib import nullcontext
import pytest
import src.utils.ehex as ehex
from src.utils.ehex import Ehex


@pytest.mark.parametrize("test_value, expected",
    [ ('0', nullcontext()),
      ( 9,  nullcontext()),
      ('F', nullcontext()),
      ( 96, pytest.raises(ValueError)),
      ( -5, pytest.raises(ValueError)),
      ('g', pytest.raises(ValueError)),
      (0.2, pytest.raises(TypeError))
    ])
def test_ehex_construction(test_value, expected):
    with expected as e:
        my_hex = Ehex(test_value)



@pytest.mark.parametrize("first, second, expected",
    [ ('2', '2', nullcontext(True)), 
      ('A',  10, nullcontext(True)),
      ('C',  12, nullcontext(True)),
      ('B', 'C', nullcontext(False)),
      ('B', 112, pytest.raises(ValueError)),
      ('B', 'b', pytest.raises(ValueError))
    ])
def test_comaparing_ehexes(first, second, expected):
    with expected as e:
        a = Ehex(first)
        b = Ehex(second)
        assert (a == b) == e



@pytest.mark.parametrize("first, second, expected",
    [ ('2', '2', nullcontext(True)), 
      ('A',  10, nullcontext(True)),
      ('C',  12, nullcontext(True)),
      ('B', 'C', nullcontext(False)),
      ('B', 112, nullcontext(False)),
      ('B', 'b', nullcontext(False)),
      ('B', -12, nullcontext(False))
    ])
def test_comparing_ehex_to_raw(first, second, expected):
    with expected as e:
        a = Ehex(first)
        assert (a == second) == e



@pytest.mark.parametrize("test_value, expected",
    [ ( 2 , True),
      ('3', True),
      (14 , True),
      ( 0 , True),
      ('A', True),
      ( 4 , False),
      ('F', False)
     ])
def test_ehex_in_raw_list(test_value, expected):
    raw_list = ['2', '3', 'E', 0, 10, 57]
    a = Ehex(test_value)
    assert (a in raw_list) == expected



@pytest.mark.parametrize("test_value, expected",
    [ ( 0, '0'),
      ( 9, '9'),
      ( 15,'F'),
    ])
def test_ehex_str(test_value, expected):
    my_hex = Ehex(test_value)
    assert str(my_hex) == expected



@pytest.mark.parametrize("test_value, expected",
    [ ( '0', 0),
      ( '9', 9),
      ( 'F', 15),
    ])
def test_ehex_int(test_value, expected):
    my_hex = Ehex(test_value)
    assert int(my_hex) == expected



@pytest.mark.parametrize("test_value, expected",
    [ ('0', nullcontext(0)), 
      ('9', nullcontext(9)), 
      ('A', nullcontext(10)), 
      ('G', nullcontext(16)),
      ( 1 , pytest.raises(TypeError)),
      ('a', pytest.raises(ValueError))
    ])
def test_hex_to_int(test_value, expected):
    with expected as e:
        assert ehex.hex_to_int(test_value) == e



@pytest.mark.parametrize("test_value, expected",
    [ (  0, nullcontext('0')), 
      (  9, nullcontext('9')), 
      ( 10, nullcontext('A')), 
      ( 16, nullcontext('G')),
      ('1', pytest.raises(TypeError)),
      ( 51, pytest.raises(ValueError)),
      ( -3, pytest.raises(ValueError))
    ])
def test_int_to_hex(test_value, expected):
    with expected as e:
        assert ehex.int_to_hex(test_value) == e



@pytest.mark.parametrize("test_value, expected",
    [ ('0', True),
      ('9', True),
      ('B', True),
      ('X', True), 
      ( 0, False),
      (-3, False),
      ( 0.1, False), 
      ("Something invalid", False)
    ])
def test_is_valid(test_value, expected):
    assert ehex.is_valid(test_value) == expected


