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
    [ (Ehex('2'), Ehex('2'), True), 
      (Ehex('A'), Ehex(10), True),
      (Ehex('C'), Ehex('C'), True),
      (Ehex('B'), Ehex('C'), False),
      (Ehex('2'), '2', True), 
      (Ehex('A'),  10, True),
      (Ehex('C'),  12, True),
      (Ehex('B'), 'C', False),
      (Ehex('B'), 112, False),
      (Ehex('B'), 'b', False),
      (Ehex('B'), -12, False)
    ])
def test_comaparison(first, second, expected):
    assert (first == second) == expected



@pytest.mark.parametrize("test_value, expected",
    [ ( Ehex(0), '0'),
      ( Ehex(9), '9'),
      ( Ehex(15),'F'),
    ])
def test_ehex_str(test_value, expected):
    assert str(test_value) == expected



@pytest.mark.parametrize("test_value, expected",
    [ ( Ehex('0'), 0),
      ( Ehex('9'), 9),
      ( Ehex('F'), 15),
    ])
def test_ehex_int(test_value, expected):
    assert int(test_value) == expected



@pytest.mark.parametrize("first, second, expected",
    [ (Ehex('0'), Ehex('A'), nullcontext(True)), 
      (Ehex('4'), Ehex('4'), nullcontext(False)), 
      (Ehex('C'), Ehex('9'), nullcontext(False)),
      (Ehex('0'), 'A', nullcontext(True)), 
      (Ehex('4'), '4', nullcontext(False)), 
      (Ehex('C'), '9', nullcontext(False)),
      (Ehex('0'), 'a', pytest.raises(ValueError)), 
      (Ehex('4'), 0.1, pytest.raises(TypeError)), 
      (Ehex('0'), 10,  nullcontext(True)), 
      (Ehex('4'), 4,   nullcontext(False)), 
      (Ehex('C'), 9,   nullcontext(False)),
      (Ehex('C'), 99,  pytest.raises(ValueError))
    ])
def test_ehex_lt(first, second, expected):
    with expected as e:
        assert (first < second) == e



@pytest.mark.parametrize("first, second, expected",
    [ (Ehex('0'), Ehex('A'), nullcontext(True)), 
      (Ehex('4'), Ehex('4'), nullcontext(True)), 
      (Ehex('C'), Ehex('9'), nullcontext(False)),
      (Ehex('0'), 'A', nullcontext(True)), 
      (Ehex('4'), '4', nullcontext(True)), 
      (Ehex('C'), '9', nullcontext(False)),
      (Ehex('0'), 'a', pytest.raises(ValueError)), 
      (Ehex('4'), 0.1, pytest.raises(TypeError)), 
      (Ehex('0'), 10,  nullcontext(True)), 
      (Ehex('4'), 4,   nullcontext(True)), 
      (Ehex('C'), 9,   nullcontext(False)),
      (Ehex('C'), 99,  pytest.raises(ValueError))
    ])
def test_ehex_le(first, second, expected):
    with expected as e:
        assert (first <= second) == e



@pytest.mark.parametrize("first, second, expected",
    [ (Ehex('0'), Ehex('A'), nullcontext(False)), 
      (Ehex('4'), Ehex('4'), nullcontext(False)), 
      (Ehex('C'), Ehex('9'), nullcontext(True)),
      (Ehex('0'), 'A', nullcontext(False)), 
      (Ehex('4'), '4', nullcontext(False)), 
      (Ehex('C'), '9', nullcontext(True)),
      (Ehex('0'), 'a', pytest.raises(ValueError)), 
      (Ehex('4'), 0.1, pytest.raises(TypeError)), 
      (Ehex('0'), 10,  nullcontext(False)), 
      (Ehex('4'), 4,   nullcontext(False)), 
      (Ehex('C'), 9,   nullcontext(True)),
      (Ehex('C'), 99,  pytest.raises(ValueError))
    ])
def test_ehex_gt(first, second, expected):
    with expected as e:
        assert (first > second) == e



@pytest.mark.parametrize("first, second, expected",
    [ (Ehex('0'), Ehex('A'), nullcontext(False)), 
      (Ehex('4'), Ehex('4'), nullcontext(True)), 
      (Ehex('C'), Ehex('9'), nullcontext(True)),
      (Ehex('0'), 'A', nullcontext(False)), 
      (Ehex('4'), '4', nullcontext(True)), 
      (Ehex('C'), '9', nullcontext(True)),
      (Ehex('0'), 'a', pytest.raises(ValueError)), 
      (Ehex('4'), 0.1, pytest.raises(TypeError)), 
      (Ehex('0'), 10,  nullcontext(False)), 
      (Ehex('4'), 4,   nullcontext(True)), 
      (Ehex('C'), 9,   nullcontext(True)),
      (Ehex('C'), 99,  pytest.raises(ValueError))
    ])
def test_ehex_ge(first, second, expected):
    with expected as e:
        assert (first >= second) == e



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


