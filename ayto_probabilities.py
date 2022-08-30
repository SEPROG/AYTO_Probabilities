import argparse
import itertools
from pprint import pprint
from typing import Any

import imgkit
import numpy as np
import pandas as pd

import instruction_handler as i_handler


def count_occurrences(permutations,
                      i_set: i_handler.InstructionSet) -> pd.DataFrame:
    occurrences = np.zeros(tuple(len(team) for team in i_set.participants), dtype=int)

    for perm in permutations:
        for pid_a in range(len(perm)):
            for participant_b in perm[pid_a]:
                occurrences[pid_a][participant_b.pid] += 1

    return pd.DataFrame(occurrences, dtype=int,
                        index=[p.name for p in i_set.participants[0]],
                        columns=[p.name for p in i_set.participants[1]])


def occurrences_for_episodes(i_set: i_handler.InstructionSet):
    perm_iter = i_set.gen_base_permutations()

    for ep_event_name in zip(i_set.episode_events, i_set.episode_names):
        for event in ep_event_name[0]:
            perm_iter = event.filter_func(perm_iter)
        perm_iter, perm_tee = itertools.tee(perm_iter)

        yield ep_event_name[1], count_occurrences(perm_tee, i_set)


def main(args: dict[str, Any]):
    # generate instruction set
    i_set = i_handler.instructions_from_txt(args['instructions_file'])
    if args['verbose']:
        pprint(args)
        print()
        i_set.print_config()
        print()

    # calculate results
    excel_results: list[tuple[str, pd.Styler]] = []
    for ep_name, occurrences in occurrences_for_episodes(i_set=i_set):
        # create styled df and preprocess values if relative flag is set
        if args['relative']:
            occurrences /= occurrences.sum()[0]

        styled = _styled_df(occurrences)
        excel_results += [(ep_name, styled)]

        if args['relative']:
            styled.format('{:.2%}')

        # output/export results
        if not args['silent']:
            print('>>> %s' % ep_name)
            print(occurrences.to_string(col_space=2 + max(7 if args['relative']
                                                          else len(str(occurrences.max().max())),
                                                          max(len(p.name) for p in i_set.participants[1])),
                                        float_format=lambda val: f'{val:.2%}'))
            print()

        if args['csv']:
            occurrences.to_csv('%s/%s.csv' % (args['csv'], ep_name))

        if args['html']:
            styled.to_html('%s/%s.html' % (args['html'], ep_name), encoding='utf16')

        if args['png']:
            # TODO: implement failsafe via matplotlib engine (mby with try/except)
            # TODO: Names can be too large for box (observe "Franziska" in AYTO VIP S2)
            imgkit.from_string(styled.to_html(encoding='utf16'), '%s/%s.png' % (args['png'], ep_name),
                               options={'--quiet': ''})

    if args['excel']:
        # append file extension if not specified (correctly)
        if args['excel'][-5:] != '.xlsx':
            args['excel'] += '.xlsx'

        with pd.ExcelWriter(args['excel']) as excel_writer:
            for ep_name, df in excel_results:
                df.to_excel(excel_writer, sheet_name=ep_name)


def _styled_df(occurrences):
    styled: pd.Styler = occurrences.style

    styled = styled.background_gradient(axis=None,
                                        cmap='cool',
                                        vmin=0,
                                        vmax=occurrences.sum()[0])
    styled = styled.highlight_between(left=0, right=0, color='lightgrey')
    # styled = styled.highlight_between(left=1, right=1, color='orange')
    # TODO: correct highlight (row/column) and ep_name
    styled = styled.set_table_styles([
        {'selector': '',
         'props': [
             ('border-collapse', 'collapse'),
             ('width', '100%'),
             ('table-layout', 'fixed')
         ]},
        {'selector': 'td,th',
         'props': [
             ('border', '1px solid dimgrey'),
             ('padding', '6px')
         ]},
        {'selector': 'th',
         'props': [
             ('background-color', 'dimgrey'),
             ('color', 'white'),
             ('font-family', 'sans-serif')
         ]},
        {'selector': 'td',
         'props': [
             ('text-align', 'right'),
             ('color', 'black'),
             ('font-family', 'monospace')
         ]}
    ])
    return styled


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculates perfect match probabilities '
                                                 'for the TV-Show "Are You The One".',
                                     epilog='For more information visit: https://github.com/SEPROG/AYTO_Probabilities')

    parser.add_argument('instructions_file', type=str,
                        help='Path of the instruction file to be parsed.')

    parser.add_argument('--png', '--img', '--image', type=str, metavar='target_folder',
                        help='Export results as .png into target_folder.')
    parser.add_argument('--html', type=str, metavar='target_folder',
                        help='Export results as .html into target_folder.')
    parser.add_argument('--csv', type=str, metavar='target_folder',
                        help='Export results as .csv into target_folder.')
    parser.add_argument('--excel', '--xls', '--xlsx', type=str, metavar='excel_file',
                        help='Export results as excel_file')

    parser.add_argument('--relative', action='store_true',
                        help='Outputs data as empirical probability instead of number of outcomes.')

    parser.add_argument('-s', '--silent',
                        action='store_true',
                        help='Silent Mode. Don\'t write to output stram.')
    parser.add_argument('-v', '--verbose',
                        action='store_true')

    main(vars(parser.parse_args()))
