""" For testing src/utils/dice.py

We test by rolling 2 of a selection of dice
We use pytest-mocker to patch randint, so that it returns a predictable 
value.
"""

import pytest
import src.utils.dice as dice

@pytest.mark.parametrize("sides, rolls, expected",
    [
        (4,  [2, 3], 5),
        (6,  [1, 5], 6),
        (8,  [5, 8], 13),
        (10, [3, 9], 12),
        (12, [2, 11], 13),
        (20, [14, 19], 33)
    ])
def test_roll(mocker, sides: int, rolls: list[int], expected: int):
    mock_randint = mocker.patch("src.utils.dice.randint")

    mock_randint.side_effect = rolls

    roll = dice.roll(2, sides)
    assert mock_randint.call_count == 2
    assert roll == expected
