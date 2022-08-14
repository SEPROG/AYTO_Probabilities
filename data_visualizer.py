from math import factorial

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.table import Table


def print_probabilities(occurrences: list[list[int]],
                        participants: tuple[list[str], list[str]],
                        relative: bool = False,
                        title: None | str = None) -> None:
    # calculate number of scenarios
    n_scenarios: int = sum(x[0] for x in occurrences)
    all_scenarios: int = factorial(len(occurrences)) * 10 ** (len(occurrences[0]) - len(occurrences))

    # gradient for cell background
    gradient = ((1.0, 0.0),  # r (100%, 0%)
                (0.0, 0.0),  # g (100%, 0%)
                (1.0, 0.8))  # b (100%, 0%)

    cell_values = [['%.2f%%' % (p * 100 / n_scenarios) if relative else str(p)
                    for p in sublist] for sublist in occurrences]
    cell_colours = [[tuple((c[0] - c[1]) * p / n_scenarios + c[1] for c in gradient)
                     for p in sublist] for sublist in occurrences]

    # create plot and set parameters
    plt.rcParams["figure.figsize"] = [20, 20]
    plt.rcParams["figure.autolayout"] = True

    fig: Figure
    ax: Axes
    fig, ax = plt.subplots(num='AYTO Probabilities' if title is None else title)
    plt.suptitle('%d / %d = %.5f%%' % (n_scenarios, all_scenarios, n_scenarios * 100 / all_scenarios))

    # create table
    table: Table = ax.table(cellText=cell_values,
                            cellColours=cell_colours,
                            cellLoc='right',
                            rowLabels=participants[0],
                            rowColours=None,
                            rowLoc='left',
                            colLabels=participants[1],
                            colColours=None,
                            colLoc='center',
                            loc='center',
                            edges='BRTL')  # substring of 'BRTL' Bottom Right Top Left

    # modify table
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1.25, 5)
    ax.axis('off')

    # show plot
    plt.show()


def print_probabilities_cli(occurrences: list[list[int]],
                            participants: tuple[list[str], list[str]],
                            relative: bool = False,
                            title: None | str = None):
    # unpack participants to set_a and set_b
    set_a, set_b = participants

    # calculate number of scenarios
    n_scenarios: int = sum(x[0] for x in occurrences)
    if title is None:
        title = str(n_scenarios)

    # calculate padding based on max length of number and max length of name (of set_b and set_add)
    pad: int = max(7 if relative else max(len(str(pp)) for p in occurrences for pp in p),
                   max(len(name) for name in set_b)) + 1

    # calculate padding for first row based on max length of name (of set_a) and title length
    pad_0: int = max(len(name) for name in set_a + [title])

    # print set_b names
    print('%s ' * (len(occurrences[0]) + 1) % (title.rjust(pad_0),
                                               *tuple(name.rjust(pad) for name in set_b)))

    # print set_a names and cell_values
    for pid_a in range(len(occurrences)):
        print('%s ' * (len(occurrences[0]) + 1) % (set_a[pid_a].rjust(pad_0),
                                                   *tuple(('%.2f%%' % (n * 100 / n_scenarios)
                                                           if relative else str(n)).rjust(pad)
                                                          for n in occurrences[pid_a])))
