""" For testing src/utils/ehex.py """

from contextlib import nullcontext
import pytest
import src.utils.ehex as ehex


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
      ( 51, pytest.raises(ValueError))
     ])
def test_int_to_hex(test_value, expected):
    with expected as e:
        assert ehex.int_to_hex(test_value) == e

@pytest.mark.parametrize("test_value, expected",
    [ ('0', True), ('9', True), ('B', True), ('X', True), 
      ( 0, False), ( 0.1, False), ("Something invalid", False) ])
def test_is_valid(test_value, expected):
    assert ehex.is_valid(test_value) == expected


