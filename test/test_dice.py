import src.dice.dice as dice

test_dice = [4, 6, 8, 10, 12, 20]
test_numbers = [
        2, 3, # for d4s
        1, 5, # for d6s
        5, 8, # for d8s
        3, 9, # for d10s
        2, 11, # for d12s
        14, 19 # for d20s
        ]
test_answers = [5, 6, 13, 12, 13, 33]

def test_roll():
    dice.randint = lambda x, y : test_numbers.pop(0)
    for test_die in test_dice:
        result = dice.roll(2, test_die)
        assert result == test_answers.pop(0)

