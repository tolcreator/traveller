""" For testing src/utils/ehex.py """

import src.utils.ehex as ehex
import pytest



@pytest.mark.parametrize("test_value, expected",
    [ ('0', 0), ('9', 9), ('A', 10), ('G', 16) ])
def test_hex_to_int(test_value, expected):
    assert ehex.hex_to_int(test_value) == expected


def test_hex_to_int_value_error():
    with pytest.raises(ValueError):
        ehex.hex_to_int("Something invalid")

def test_hex_to_int_type_error():
    with pytest.raises(TypeError):
        """ Looks sort of right, but it isn't """
        ehex.hex_to_int(1)


@pytest.mark.parametrize("test_value, expected",
    [ (0, '0'), (8, '8'), (11, 'B'), (17, 'H') ])
def test_int_to_hex(test_value, expected):
    assert ehex.int_to_hex(test_value) == expected

def test_int_to_hex_value_error():
    with pytest.raises(ValueError):
        """ Out of bounds """
        ehex.int_to_hex(51)

def test_int_to_hex_type_error():
    with pytest.raises(TypeError):
        """ Looks sort of right, but it isn't """
        ehex.int_to_hex('2')

@pytest.mark.parametrize("a, b, expected",
    [ ('4', '2', True), ('A', '9', True), ('X', 'L', True), 
      ('3', 'C', False), ('5', '5', False) ])
def test_greater_than(a, b, expected):
    assert ehex.greater_than(a, b) == expected

@pytest.mark.parametrize("a, b, expected",
    [ ('4', '2', True), ('A', '9', True), ('X', 'L', True), 
      ('3', 'C', False), ('5', '5', True) ])
def test_greater_than_or_equal_to(a, b, expected):
    assert ehex.greater_than_or_equal_to(a, b) == expected

@pytest.mark.parametrize("a, b, expected",
    [ ('2', '4', True), ('9', 'A', True), ('L', 'X', True), 
      ('C', '3', False), ('5', '5', False) ])
def test_less_than(a, b, expected):
    assert ehex.less_than(a, b) == expected

@pytest.mark.parametrize("a, b, expected",
    [ ('2', '4', True), ('9', 'A', True), ('L', 'X', True), 
      ('C', '3', False), ('5', '5', True) ])
def test_less_than_or_equal_to(a, b, expected):
    assert ehex.less_than_or_equal_to(a, b) == expected

@pytest.mark.parametrize("test_value, expected",
    [ ('0', True), ('9', True), ('B', True), ('X', True), 
      ( 0, False), ( 0.1, False), ("Something invalid", False) ])
def test_is_valid(test_value, expected):
    assert ehex.is_valid(test_value) == expected



