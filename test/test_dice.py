""" For testing src/utils/dice.py

We test by rolling 2 of a selection of dice
We overwrite dice.randint so that we get predictable results
We then compare the results with the expected values
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
def test_roll(sides: int, rolls: list[int], expected: int):
    dice.randint = lambda x, y : rolls.pop(0)
    assert dice.roll(2, sides) == expected
