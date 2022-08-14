from itertools import permutations, product
from typing import TypeAlias, Iterable

import data_visualizer as vis
import name_translation as nt

t_matches: TypeAlias = list[int]
t_scenario: TypeAlias = list[t_matches]
t_matchbox_info: TypeAlias = tuple[list[t_matches], list[t_matches]]  # first no-match second perf-match


# TODO: compute in parallel

# TODO: add return types (is generator but idk the correct declaration)
def gen_base_scenarios(set_b: list[int]):
    for perm_b in permutations(set_b):
        yield [[pid_b] for pid_b in perm_b]  # TODO: this is correct idk why ide says no


# TODO: add return types (it's generator but idk the correct declaration)
def gen_all_scenarios(participants: nt.t_participants):
    # create PIDs (Participant IDs) for set_a, set_b and set_add
    set_a, set_b, set_add = tuple(list(range(len(s))) for s in participants)
    len_b = len(set_b)

    # set_add IDs are shifted to fit set_b
    set_add = [add_index + len(set_b) for add_index in set_add]
    len_add = len(set_add)

    for perm_b in gen_base_scenarios(set_b):
        for prod in product(set_b, repeat=len_add):
            perm_add = [[]] * len_b
            for i in range(len_add):
                perm_add[prod[i]] = perm_add[prod[i]] + [set_add[i]]

            # return scenario by combining permutation of set_b and set_add
            yield [matches[0] + matches[1] for matches in zip(perm_b, perm_add)]


# TODO add return type
def create_generators():
    g = [gen_all_scenarios(nt.participants)]
    g += [filter_match_box(g[-1], nt.match_box)]
    for result in nt.match_nights:
        g += [filter_match_night(g[-1], result)]
    return g


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


def main() -> None:
    g = create_generators()

    occurrences: list[list[int]] = count_occurrences(g[-1])
    participants = (nt.participants[0],
                    [name for pset in nt.participants[1:] for name in pset])

    vis.print_probabilities(occurrences, participants, True, title='AYTO Probabilities')

    vis.print_probabilities_cli(occurrences, participants, False)
    print()
    vis.print_probabilities_cli(occurrences, participants, True)


if __name__ == '__main__':
    main()
