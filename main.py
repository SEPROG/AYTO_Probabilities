import json
import sys
from itertools import permutations, product
from typing import TypeAlias, Iterable

import data_visualizer as vis
import name_translation as nt

t_matches: TypeAlias = list[int]
t_scenario: TypeAlias = list[t_matches]
t_matchbox_info: TypeAlias = tuple[list[t_matches], list[t_matches]]  # first no-match second perf-match

generated: int = 0


# TODO: add more custom(-izable) filtering mechanisms


# TODO: add return types (it's generator but idk the correct declaration)
def gen_all_scenarios(participants: nt.t_participants):
    set_a, set_b, set_add = tuple(list(range(len(s))) for s in participants)
    set_add = [add_index + len(set_b) for add_index in set_add]
    global generated

    # TODO: rename x, y and a
    for x in gen_base_scenarios(set_b):
        for y in product(set_b, repeat=len(set_add)):
            a = [[]] * len(x)
            for i in range(len(y)):
                a[y[i]] = a[y[i]] + [set_add[i]]
            generated += 1
            yield [x[j] + a[j] for j in range(len(x))]


# TODO: rename x and y
# TODO: add return types (is generator but idk the correct declaration)
def gen_base_scenarios(set_b: list[int]):
    for x in permutations(set_b):
        yield [[y] for y in x]  # TODO: this is correct idk why ide says no


def filter_match_box(scenarios: Iterable[t_scenario],
                     matchbox_info: t_matchbox_info) -> filter:
    return filter(lambda scenario:
                  all(all(pid_2 not in x[1] for pid_2 in x[0]) and
                      all(pid_2 in x[0] for pid_2 in x[2])
                      for x in zip(scenario, *matchbox_info)),
                  scenarios)


def filter_match_night(scenarios: Iterable[t_scenario],
                       result: nt.t_match_night) -> filter:
    return filter(lambda scenario:
                  sum(x[0] in x[1] for x in zip(result[0], scenario)) == result[1],
                  scenarios)


def count_occurrences(scenarios: Iterable[t_scenario]) -> list[list[int]]:
    occurrences: list[list[int]] = [[0] * len(nt.participants[1] + nt.participants[2])
                                    for _ in range(len(nt.participants[0]))]
    for scenario in scenarios:
        for pid_a in range(len(scenario)):
            for pid_b in scenario[pid_a]:
                occurrences[pid_a][pid_b] += 1

    return occurrences


def main():
    g = create_generators()

    occurrences: list[list[int]] = count_occurrences(g[-1])
    vis.print_probabilities(occurrences, True, title='AYTO Probabilities')

    vis.print_probabilities_cli(occurrences, False)
    print()
    vis.print_probabilities_cli(occurrences, True)


# TODO add return type
def create_generators():
    g = [gen_all_scenarios(nt.participants)]
    g += [filter_match_box(g[-1], nt.match_box)]
    for result in nt.match_nights:
        g += [filter_match_night(g[-1], result)]
    return g


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            nt.participants, nt.match_box, nt.match_nights = tuple(json.load(f))
    main()
