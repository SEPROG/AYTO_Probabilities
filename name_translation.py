from typing import TypeAlias

t_participants: TypeAlias = tuple[list[str], list[str], list[str]]
t_match_night: TypeAlias = tuple[list[int], int]
t_match_box: TypeAlias = tuple[list[list[int]], list[list[int]]]

# Testing Values
participants: t_participants = (
    # set a
    # scenarios are NOT based on this set. This is set only serves for translation from pid to name
    # scenario participant ids (named "pid") start at 0
    ['Male PID %i' % i for i in range(10)],

    # set b (same sex as set additional)
    # scenarios are calculated based on this set (and set additional)
    # scenario participant ids (named "pid") start at 0
    ['Female PID %i' % i for i in range(10)],

    # set additional (same sex as set b)
    # scenarios are calculated based on this set (and set b)
    # scenario participant ids (named "pid") start at len(set_b)
    ['TBA']
)

match_box: t_match_box = (
    [[], [], [], [], [], [], [], [], [4], []],
    [[], [0], [], [], [], [], [], [], [], []]
)

match_nights: list[t_match_night] = [
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0),
    ([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], 0),
    ([9, 8, 7, 6, 5, 4, 3, 2, 1, 10], 1)
]

# AYTO VIP S2
participants = (
    ['Amadu', 'Calvin', 'Fabio', 'Luca', 'Lukas', 'Martin', 'Maurice', 'Max', 'Michael', 'Pharrell'],
    ['Anna', 'Cecilia', 'Celina', 'Franziska', 'Gina', 'Isabelle', 'Karina', 'Luisa', 'Ricarda', 'Zoe'],
    []
)

match_box = (
    [[], [], [], [], [], [9], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], []]
)

match_nights = [
    ([1, 4, 7, 9, 5, 2, 8, 3, 0, 6], 3),
]

# AYTO S3
# participants = (
#    ['Andre', 'Antonio', 'Dustin', 'Jordi', 'Leon', 'Marius', 'Max', 'Mike', 'Tim', 'William'],
#    ['Dana', 'Estelle', 'Isabelle', 'Jessica', 'Joelina', 'Kerstin', 'Marie', 'Monami', 'Raphaela', 'Zaira'],
#    ['Desirée']
# )
#
# match_box: t_match_box = (
#    [[8], [7], [], [], [7], [], [3], [3], [], []],
#    [[], [], [], [], [], [9], [], [], [], []]
# )
#
# match_nights: list[t_match_night] = [
#    ([8, 7, 9, 1, 3, 2, 5, 4, 6, 0], 3),
#    ([0, 7, 2, 9, 1, 6, 5, 4, 3, 8], 2),
#    ([8, 5, 9, 3, 1, 2, 7, 4, 6, 0], 2),
#    ([2, 7, 9, 8, 1, 3, 6, 4, 5, 0], 3),
#    ([4, 5, 2, 9, 3, 8, 7, 1, 10, 0], 2),
#    ([6, 0, 2, 10, 3, 9, 5, 1, 4, 8], 4),
#    ([10, 0, 2, 7, 3, 9, 6, 4, 5, 8], 6),
# ]
